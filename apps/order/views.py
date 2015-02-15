#coding:UTF-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
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

def order_list(request):                                                         #kim                                     
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
   # session = '10E5C27B3AA37718CFF61A6CA32135196E4636F6500251D3801C302B9F68B58F'
    if authuri:
        return HttpResponseRedirect(authuri)
    order_list_result = api_list.list_my_product_order(request,session)          
    if not order_list_result or order_list_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_list_result)    
    try:
        meta_data = {"order_list":order_list_result["productOrderList"]}
        return render(request,"order/orders.html",meta_data)
    except Exception,e:
        print e
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__, e)


def order_detail(request,order_id):                                            #kim
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    #session = '10E5C27B3AA37718CFF61A6CA32135196E4636F6500251D3801C302B9F68B58F'
    if authuri:
        return HttpResponseRedirect(authuri)
    order_detail_result = api_list.get_product_order(request, session, order_id)
   # cart_num = api_list.get_goods_num_in_cart(request)
    if not order_detail_result or order_detail_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_detail_result)
    try:
        process_order_detail(order_detail_result)
        meta_data = {"order":order_detail_result}
        return render(request,"order/order.html",meta_data)
    except Exception,e:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)

def process_order_detail(data):
    if data["productOrder"].get("creationTime"):
        time_tuple = time.localtime(data["productOrder"]["creationTime"]/1000)
        data["productOrder"]["creationTime"] =  time.strftime("%Y-%m-%d %H:%M",time_tuple)
    
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
    cartInfo = request.REQUEST.get('cartInfo')
    paymentId = request.REQUEST.get('paymentId')
    if not cartInfo:
       return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品")

    try:
       cart_dict = json.loads(cartInfo)
       if not cart_dict:
           return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品")
    except Exception,e:
       print e
       return response_data_utils.error_response(request, "没有选择商品！", __name__, "没有选择商品")
    
    result = api_list.submit_order(request, session, cartInfo , contact,  address,  contactPhone)
    order_id = 0
    alipay_sign = ""
    if result and result.get("orderId"):
        order_id = result.get("orderId")
        alipay_sign = result.get("webAlipaySign")
    else:
        return response_data_utils.error_response(request, result.get("errorString"), __name__, result)
    if order_id == 0:
        return response_data_utils.error_response(request, "服务器忙，请稍后重试！", __name__, result)
    
    order_info = api_list.get_product_order(request, session, order_id) 
    meta_data = {"order_id": order_id}
    if order_info and order_info.get("productOrder"):
        product_order = order_info.get("productOrder") 
        meta_data["goods_num"] = product_order.get("goodsNum")
        meta_data["total_fee"] = product_order.get("totalFee")
    return render(request, 'order/choice_bank.html', meta_data)

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
    print "====================="
    print pay_code
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
    return_url = "http://wxtest.fenpuwang.com/order/detail/" + agent_bill_id
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
    print sign_str
    print agent_bill_time
    print sign
    return meta_data
