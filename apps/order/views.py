#coding:UTF-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from apps.api import api_list
from apps.utils import data_process_utils,string_utils, response_data_utils, weixin_auth_utils
import requests
import json
import cgi
import logging
import time

logger = logging.getLogger('django')

def order_pay_test(request):
    return render(request,"order/pay.html")

def order_pay_result(request, order_id, pay_status=0):
    user_info = weixin_auth_utils.get_user_info(request)
    session = user_info.get('session')
    if not order_id:
        return response_data_utils.error_response(request, "找不到对应的订单！", __name__)
    meta_data = {'paySuccess':pay_status, 'order_id':order_id}
    return weixin_auth_utils.fp_render(request,'order/order_pay_result.html',meta_data, session)

def ajax_order_list(request,mark=0):                                                         #kim                                     
    is_ajax = request.is_ajax()
    if not is_ajax:
        return response_data_utils.error_response(request, "非法请求！",__name__, "not ajax")
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return response_data_utils.error_response(request, "非法请求！",__name__, "not ajax", session)
    try: 
        order_list_result = api_list.list_my_product_order(request,session,mark)          
        if not order_list_result or order_list_result["error"]!=0:
            return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_list_result, session)    
        process_order_detail(order_list_result)
        next_request_url = ""
        if str(order_list_result['mark']) != "0":
           next_request_url = reverse('order:ajax_order_list', kwargs ={"mark":order_list_result['mark']})
        meta_data = {'url':next_request_url, "order_list":order_list_result["productOrderList"], "from_ajax":1}
        context = RequestContext(request, meta_data)
        template = loader.get_template('order/orders_list.html')
        response_json = {'html':template.render(context), 'url':next_request_url}
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    except Exception,e:
        print e
        return response_data_utils.error_response(request, "推荐产品不存在！",__name__, e, session)

def order_list(request):                                                         #kim                                     
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
   # session = '10E5C27B3AA37718CFF61A6CA32135196E4636F6500251D3801C302B9F68B58F'
    if authuri:
        return HttpResponseRedirect(authuri)
    order_list_result = api_list.list_my_product_order(request,session)          
    if not order_list_result or order_list_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_list_result, session)    
    try:
        process_order_detail(order_list_result)
        next_request_url = ""
        if str(order_list_result['mark']) != "0":
           next_request_url = reverse('order:ajax_order_list', kwargs ={"mark":order_list_result['mark']})
        meta_data = {'url':next_request_url, "nav":"order","order_list":order_list_result["productOrderList"]}
        return weixin_auth_utils.fp_render(request,'order/orders.html',meta_data, session)
    except Exception,e:
        print e
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__, e, session)


def order_detail(request,order_id):                                            #kim
    user_agent = request.META.get('HTTP_USER_AGENT')
    is_mm = 0
    user_agent = user_agent.lower()
    if "micromessenger" in user_agent:
      is_mm = 1

    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    #session = '10E5C27B3AA37718CFF61A6CA32135196E4636F6500251D3801C302B9F68B58F'
    if authuri:
        return HttpResponseRedirect(authuri)
    order_detail_result = api_list.get_product_order(request, session, order_id)
   # cart_num = api_list.get_goods_num_in_cart(request)
    if not order_detail_result or order_detail_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_detail_result, session)
    try:
        process_order_detail(order_detail_result)
        meta_data = {"order":order_detail_result, 'navTitle':'订单详情','search_btn':1 , 'is_mm':is_mm}
        return weixin_auth_utils.fp_render(request,'order/order.html',meta_data, session)
    except Exception,e:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e, session)

def process_order_detail(data):
    if data.get("productOrder") and data.get("productOrder").get("creationTime"):
        time_tuple = time.localtime(data["productOrder"]["creationTime"]/1000)
        data["productOrder"]["creationTime"] =  time.strftime("%Y-%m-%d %H:%M",time_tuple)
    if data.get("productOrderList"):
        for order in data["productOrderList"]:
            if order.get("creationTime"):
               time_tuple = time.localtime(order["creationTime"]/1000)
               order["creationTime"] = time.strftime("%Y-%m-%d %H:%M",time_tuple)

def submit_order(request) :
    #return render(request, 'order/choice_bank.html', {})
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return HttpResponseRedirect(authuri)
    contact = request.REQUEST.get('contact')
    contactPhone =request.REQUEST.get('contactPhone')
    address = request.REQUEST.get('address')
    remark = request.REQUEST.get('remark')
    cartInfo = request.REQUEST.get('cartInfo')
    payment = request.REQUEST.get('payment')
    orderId = request.REQUEST.get('orderId')
    if not orderId:
       if not cartInfo:
           return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品", session)
       try:
           cart_dict = json.loads(cartInfo)
           if not cart_dict:
               return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品", session)
       except Exception,e:
           print e
           return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品", session)
    
       result = api_list.submit_order(request, session, cartInfo , contact,  address,  contactPhone, remark)
       orderId = 0
       if result and result.get("orderId"):
           orderId = result.get("orderId")
       else:
           return response_data_utils.error_response(request, result.get("errorString"), __name__, result, session)
    
    if orderId == 0:
        return response_data_utils.error_response(request, "服务器忙，请稍后重试！", __name__, result, session)

    order_info = api_list.get_product_order(request, session, orderId) 
    if not order_info or order_info["error"]!=0:
        return response_data_utils.error_response(request, "找不到对应的订单！", __name__, order_info, session)

    meta_data = {"order_id": orderId}
    if order_info and order_info.get("productOrder"):
        product_order = order_info.get("productOrder") 
        meta_data["goods_num"] = product_order.get("goodsNum")
        meta_data["total_fee"] = product_order.get("totalFee")

    if payment == "0":
        alipay_url = reverse("order:alipay_order",kwargs={})
        return HttpResponseRedirect(alipay_url + "?orderId=" + str(orderId) +"&session=" + session )
    elif payment == "1":
        meta_data["navTitle"] = "选择银行"
        meta_data["search_btn"] = 1
        return weixin_auth_utils.fp_render(request,'order/choice_bank.html',meta_data, session)
    elif payment == "2": 
        wxpay_url = reverse("order:wxpay_order",kwargs={})
        return HttpResponseRedirect(wxpay_url + "?orderId=" + str(orderId) +"&session=" + session )

def to_pay_order(rquest):
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return HttpResponseRedirect(authuri)
    payment = request.REQUEST.get('payment')
    orderId = request.REQUEST.get('orderId')
    if not orderId:
        return response_data_utils.error_response(request, "服务器忙，请稍后重试！", __name__, result, session)
    if orderId == 0:
        return response_data_utils.error_response(request, "服务器忙，请稍后重试！", __name__, result, session)

    order_info = api_list.get_product_order(request, session, orderId) 
    if not order_info or order_info["error"]!=0:
        return response_data_utils.error_response(request, "找不到对应的订单！", __name__, order_info, session)

    meta_data = {"order_id": orderId}
    if order_info and order_info.get("productOrder"):
        product_order = order_info.get("productOrder") 
        meta_data["goods_num"] = product_order.get("goodsNum")
        meta_data["total_fee"] = product_order.get("totalFee")

    if payment == "0":
        alipay_url = reverse("order:alipay_order",kwargs={})
        return HttpResponseRedirect(alipay_url + "?orderId=" + str(orderId) +"&session=" + session )
    elif payment == "1":
        meta_data["navTitle"] = "选择银行"
        meta_data["search_btn"] = 1
        return weixin_auth_utils.fp_render(request,'order/choice_bank.html',meta_data, session)
    elif payment == "2": 
        wxpay_url = reverse("order:wxpay_order",kwargs={})
        return HttpResponseRedirect(wxpay_url + "?orderId=" + str(orderId) +"&session=" + session )


def ajax_submit_order(request) :
    is_ajax = request.is_ajax()
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    response_json = {'error':1, "errorString": "没有选择商品" }
    if authuri:
        response_json = {'error':2, "errorString": "需要重新授权", "authuri":authuri }
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    contact = request.REQUEST.get('contact')
    contactPhone =request.REQUEST.get('contactPhone')
    address = request.REQUEST.get('address')
    remark = request.REQUEST.get('remark')
    cartInfo = request.REQUEST.get('cartInfo')
    payment = request.REQUEST.get('payment')
    orderId = request.REQUEST.get('orderId')
    if not cartInfo:
        response_data_utils.error_log(request, "没有选择商品！", __name__, "没有选择商品")
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    try:
       cart_dict = json.loads(cartInfo)
       if not cart_dict:
          response_data_utils.error_log(request, "没有选择商品！", __name__, "没有选择商品")
          return HttpResponse(json.dumps(response_json), content_type="application/json")
    except Exception,e:
       response_data_utils.error_log(request, "没有选择商品" , __name__ , e)
       return HttpResponse(json.dumps(response_json), content_type="application/json")
    
    result = api_list.submit_order(request, session, cartInfo , contact,  address,  contactPhone, remark)
    orderId = 0
    if result and result.get("orderId"):
        orderId = result.get("orderId")
    else:
        response_data_utils.error_log(request, result.get("errorString") , __name__ , result)
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    
    if orderId == 0:
        response_json = {'orderId':orderId, 'error':0 }
        return response_data_utils.error_response(request, "服务器忙，请稍后重试！", __name__, result)

    response_json = {'orderId':orderId, 'error':0 }
    return HttpResponse(json.dumps(response_json), content_type="application/json")

def wxpay_order(request):
    show_qrcode = 0;
    if 'pay_from' in request.session and request.session['pay_from'] == 'subscribe':
      show_qrcode = 1

    session = request.REQUEST.get('session')
    order_id = request.REQUEST.get('orderId')
    user_agent = request.META.get('HTTP_USER_AGENT')
    order_info = api_list.get_product_order(request, session, order_id)
    meta_data = {}
    meta_data['order_id'] = order_id;
    meta_data['show_qrcode'] = show_qrcode;
    if order_info and order_info.get("productOrder"):
      product_order = order_info.get("productOrder");
      meta_data["wxJsApiParameters"] = product_order.get("wxJsApiParameters"); 
      meta_data["wxQrcodeUrl"] = product_order.get("wxQrcodeUrl");
      meta_data["totalFee"] = product_order.get("totalFee");
      meta_data["goodsDesc"] = product_order.get("goodsDesc");
    return render(request, 'order/order_wx_pay.html', meta_data);

def alipay_order(request):
    session = request.REQUEST.get('session')
    order_id = request.REQUEST.get('orderId')
    user_agent = request.META.get('HTTP_USER_AGENT')
    is_mm = None
    user_agent = user_agent.lower()
    if "micromessenger" in user_agent:
        is_mm = 1
    order_info = api_list.get_product_order(request, session, order_id)
    meta_data = {"is_mm": is_mm}
    if order_info and order_info.get("productOrder"):
        product_order = order_info.get("productOrder") 
        paymentHTML = product_order.get("webPayInfo"); 
        meta_data['paymentHTML'] = paymentHTML
        return render(request, 'order/order_ali_pay.html', meta_data)
    else:
        return response_data_utils.error_response(request, order_info.get("errorString"), __name__, order_info)

def pay_order(request):
    agent_bill_id = request.REQUEST.get("order_id") 
    pay_amt = request.REQUEST.get("total_fee") 
    pay_code = request.REQUEST.get("bank_type") 
    goods_num = request.REQUEST.get("goods_num")
    meta = {}
    meta["order_id"] = agent_bill_id
    meta["total_fee"] = pay_amt
    meta["bank_type"] = pay_code
    meta["goods_num"] = goods_num
    meta_data = build_huifubao_meta(meta) 
    return render(request, 'order/order_pay.html', meta_data)

def build_huifubao_meta(meat_dict):
    agent_bill_id = meat_dict.get("order_id") 
    pay_amt = meat_dict.get("total_fee") 
    pay_code = meat_dict.get("bank_type") 
    goods_num = meat_dict.get("goods_num") 
    user_ip = "114_243_214_122"

    version = "1"
    agent_id = "1956513"  #汇付宝商户id
    key = "1A5D243267734BD68DB904EA" #商户秘钥
    agent_bill_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    pay_type = "20" 
    notify_url = "http://api.dabanniu.com/v2/huifubao/dbnNotify.do"
    return_url = "http://m.fenpuwang.com/order/detail/" + agent_bill_id
    goods_name = "0000"
    goods_note = ""
    remark = ""
    agent_bill_id = "po_" + agent_bill_id + "-" + str(int(time.time()*1000))
    # 计算md5签名
    sign_str = ""
    sign_str += 'version=' + version;
    sign_str += '&agent_id=' + agent_id;
    sign_str += '&agent_bill_id=' + agent_bill_id;
    sign_str += '&agent_bill_time=' + agent_bill_time;
    sign_str += '&pay_type=' + pay_type;
    sign_str += '&pay_amt=' + pay_amt;
    sign_str += '&notify_url=' + notify_url;
    sign_str += '&return_url=' + return_url;
    sign_str += '&user_ip=' + user_ip;
    sign_str += '&key=' + key;
    
    sign = string_utils.get_md5(sign_str)
    meta_data = {'version':version, 'agent_id':agent_id, 'agent_bill_id':agent_bill_id, 'agent_bill_time':agent_bill_time,\
	         'pay_type':pay_type, 'pay_code':pay_code, 'pay_amt':pay_amt, 'notify_url':notify_url, 'return_url':return_url,\
		 'user_ip':user_ip, 'goods_name':goods_name, 'goods_num':goods_num, 'goods_note':goods_note, "remark":remark, "sign":sign}
    return meta_data
