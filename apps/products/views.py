# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from apps.api import api_list
import requests
from apps.utils import string_utils, response_data_utils, weixin_auth_utils
from apps.api import api_list, static_data
from django.core.urlresolvers import reverse
import json
import logging
import time

logger = logging.getLogger('django')
def products_index(request):
    data = static_data.get_products_index_data() 
    meta_data = response_data_utils.pack_data(request, {'data': data ,'nav':'products'})
    return render(request, 'products/products_index.html', meta_data)

def products_recommend_list(request,mark=0):                                                        #kim 
    is_ajax = request.is_ajax()
    if not is_ajax:
        return response_data_utils.error_response(request, "非法请求！",__name__, "not ajax")
    products_feature_result = api_list.get_feature_product_list(request,6 ,mark)
    if not products_feature_result or products_feature_result['error']!=0:
        return response_data_utils.error_response(request,"推荐产品不存在",__name__,products_feature_result)
    try: 
        process_products_feature(products_feature_result)
        next_request_url = ""
        if str(products_feature_result['mark']) != "0":
           next_request_url = reverse('products:products_recommend_list', kwargs ={"mark":products_feature_result['mark']})
        meta_data = {'url':next_request_url, "products_feature_list":products_feature_result.get('productList')}
        context = RequestContext(request, meta_data)
        template = loader.get_template('products/products_recommend_list.html')
        response_json = {'html':template.render(context), 'url':next_request_url}
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    except Exception,e:
        print e
        return response_data_utils.error_response(request, "推荐产品不存在！",__name__, e)

def session(request):
    #设置session
    pay_from = request.REQUEST.get('pay_from') 
    if pay_from != None and pay_from != "":
      request.session['pay_from'] = pay_from
    return HttpResponse("set session success", content_type="application/json")

def products_recommend(request):                                    #kim
    dp = request.REQUEST.get('dp')
    #微信中用户信息获取及授权处理
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')

    user_agent = request.META.get('HTTP_USER_AGENT')
 
    is_mm = None
    user_agent = user_agent.lower()
    if "micromessenger" in user_agent:
      is_mm = 1

    if authuri and is_mm == 1 and dp != None and dp != "":
      return HttpResponseRedirect(authuri)

    if dp != "" and dp != None:
      api_list.bind_user(request, session, dp)
    else:
      dp = None
    # end 

    flash_activity = api_list.get_flash_banner(request)
    products_feature_result = api_list.get_feature_product_list(request)
    cart_num_json = api_list.get_goods_num_in_cart(request, session)
    album_list = api_list.get_list_product_album(request)
    if ( not flash_activity ) or flash_activity['error'] != 0:
        return response_data_utils.error_response(request, "秒杀产品不存在", __name__, flash_activity, session)
    if ( not products_feature_result ) or products_feature_result['error'] != 0:
        return response_data_utils.error_response(request, "推荐产品不存在", __name__, products_feature_result, session)
    if (not album_list) or album_list["error"] !=0:
        return response_data_utils.error_response(request, "产品合集不存在", __name__, album_list, session)
    try: 
        process_products_feature(products_feature_result)
        next_request_url = ""
        if str(products_feature_result['mark']) != "0":
           next_request_url = reverse('products:products_recommend_list', kwargs ={"mark":products_feature_result['mark']})

        cartNum = 0
        if cart_num_json and cart_num_json['error'] == 0:
           cartNum = cart_num_json["totalNum"]
        if album_list and album_list["error"] == 0:
            for letter in album_list["result"]:
                if letter["type"] == 0:
                    album_list_little = letter["albums"]
                if letter["type"] == 1:
                    album_list_more = letter["albums"]
        meta_data = {'cartNum':cartNum,'url':next_request_url, 'nav':'products',"flash_activity":flash_activity.get('activityList'),"products_feature_list":products_feature_result.get('productList'),"album_list_little":album_list_little,"album_list_more":album_list_more}
        meta_data = response_data_utils.pack_data(request, meta_data)
        return weixin_auth_utils.fp_render(request,'products/products_recommend.html', meta_data, session)
    except Exception,e:
        return response_data_utils.error_response(request, "推荐产品不存在！",__name__, e, session)

def album_detail(request,albumId):                                                      #kim
    dp = request.REQUEST.get('dp')
    #微信中用户信息获取及授权处理
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    user_agent = request.META.get('HTTP_USER_AGENT')

    is_mm = None
    user_agent = user_agent.lower()
    if "micromessenger" in user_agent:
        is_mm = 1

    if authuri and is_mm == 1 and dp != None and dp != "":
        return HttpResponseRedirect(authuri)

    if dp != "" and dp != None:
        api_list.bind_user(request, session, dp)
    else:
        dp = None
    # end
    album_info = api_list.get_list_product_album_info(request,albumId)
    cart_num_json = api_list.get_goods_num_in_cart(request, session)
    cartNum = 0
    if not album_info and album_info["error"] !=0:
        return response_data_utils.error_response(request, "合集产品不存在！",__name__, e, session)   
    if cart_num_json and cart_num_json["error"] == 0:
        cartNum = cart_num_json["totalNum"]
    try:
        if album_info and album_info["error"] ==0:
            meta_data = {"cartNum":cartNum,"album_description":album_info["album"],"album_info":album_info["albumInfos"],"navTitle":album_info["album"]["title"]}
            return render(request,"products/album_info.html",meta_data)   
    except Exception,e:
        print "============="
        print e
        print "============="

def process_products_promote(data):                                                 #kim
    for product in data['productList']:
        pics = product.get('pics')
        if pics:
            product['org'] = pics[0]['org']

def process_products_feature(data):                                                  #kim                                                  
    for product in data['productList']:
        pics = product.get('pics')
        if pics and len(pics)>0:
            product['thumb_s'] = pics[0]['thumb-b']
        if not product.get("name_decoration"):
            product["name_decoration"]=""

# Create your views here.
def productlist_by_category(request, type=0,category_id=0,order=5,filter=0,mark=0):
    is_ajax = request.is_ajax()
    try:
        products_result = api_list.get_product_by_category(request, type, order, category_id, filter, 10, mark)
        if products_result['error'] == 0 :
            process_product_data(products_result)
            next_request_url = ""
            if str(products_result['mark']) != "0":
                next_request_url = reverse('products:query_by_all', kwargs ={"type":type, "category_id":category_id, "order":order, "filter":filter, "mark":products_result['mark']})
            meta_data = {'productList' : products_result["productList"], 'url':next_request_url ,'nav':'products'}
            if is_ajax:
                context = RequestContext(request, meta_data)
                template = loader.get_template('products/product_list.html')
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                meta_data = dict(meta_data.items() + {"type":type, "category_id":category_id, "order":str(order), "filter":filter}.items())
                meta_data = response_data_utils.pack_data(request, meta_data)
                return render(request, 'products/products.html', meta_data)
    except Exception,e:
        return response_data_utils.error_response(request, "该分类下没有产品！",  __name__, e)

def process_product_data(product_data):
    for product in product_data['productList']:
        pics = product.get('pics')
        product['goodReviewRatio'] =  int(product['goodReviewRatio']*100)
        if pics and len(pics) > 0 :
            product['thumb_s'] = pics[0]['thumb-s']

def seckill(request):
    user_from = request.REQUEST.get('from')
    if user_from == None or user_from == "":
      user_from = "flashweb"

    user_agent = request.META.get('HTTP_USER_AGENT')
    is_fenpu = 0
    user_agent = user_agent.lower()
    if "fenpuwebview" in user_agent:
      is_fenpu = 1

    seckill_result = api_list.get_flash_product_list(request)
    seckill_today_list = seckill_result["todayProductList" ]
    seckill_process(seckill_today_list)
    seckill_tomorrow_list = seckill_result["tomorrowProductList"]
    seckill_process(seckill_tomorrow_list)
    is_flashing = 0
    if seckill_today_list and len(seckill_today_list)>0:
       is_flashing = 1
#    seckill_today_list = {}
    server_time_stamp = seckill_result['timeStamp']
    meta_data = {"is_flashing":is_flashing, "seckill_today_list":seckill_today_list,"seckill_tomorrow_list":seckill_tomorrow_list,'navTitle':'秒杀', "server_time_stamp": server_time_stamp, "is_fenpu":is_fenpu, "is_url":1, "nav_url":'/11286', "user_from":user_from}
#    meta_data = {"seckill_today_list":seckill_tomorrow_list,"seckill_tomorrow_list":seckill_tomorrow_list, "server_time_stamp": server_time_stamp}
    #if seckill_today_list:
    #    return render(request,"products/flashing.html",meta_data)
    #else:
    #    return render(request,"products/flash_list.html",meta_data)
    return render(request,"products/flashing.html",meta_data)

def ajax_get_stock(request):
    is_ajax = request.is_ajax()
    seckill_result = api_list.get_flash_product_list(request)
    #seckill_today_list = seckill_result["tomorrowProductList"]
    seckill_today_list = seckill_result["todayProductList" ]
    stock_data = seckill_stock_process(seckill_today_list)
    #sold_time = seckill_sold_time_process(seckill_today_list)
    meta_data = {"error":0 ,"list": stock_data}
    return HttpResponse(json.dumps(meta_data), content_type="application/json")

def ajax_exists_qualification(request):
    session = request.REQUEST.get('session')
    if not session:
        session = request.COOKIES.get("session")
    product_uri = 'http://m.fenpuwang.com/products/'
    authuri = weixin_auth_utils.build_auth_uri(product_uri)
    is_ajax = request.is_ajax()
    if not session:
        response_json = {'error': 2,"authuri":authuri}
        print response_json
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    if not is_ajax:
        return response_data_utils.error_response(request, "非ajax!",  __name__, "no ajax")
    response_json = api_list.exists_qualification(request,session)
    print response_json
    return HttpResponse(json.dumps(response_json), content_type="application/json")

def seckill_process(data):
    for letter in data:
#        letter['flashing'] = 1
        letter["img"] = letter["pics"][0]["org"]
        letter["start_time"] = letter["flash_start_time"]
        letter["continue_time"] = letter["flash_duration"]
        letter["remaining_stock"] = letter["stock"] - letter["sold_num"] 
        if letter["remaining_stock"] < 0 :
             letter["remaining_stock"] = 0
 #       letter["start_time"] = 1427528202280
#        letter["continue_time"] = 300000
        #letter["remaining_stock"] = 0
        letter["discount"] = round(letter["flash_sizes"]["price"]/letter["price"]*10 ,1)
        for le in letter["goods"]:
            le["last_sold_time"] = time.strftime("%H:%M",time.localtime(le["last_sold_time"]/1000))
                


def seckill_stock_process(data):
    stock_data = {}
    for letter in data:
        letter["remaining_stock"] = letter["stock"] - letter["sold_num"] 
        if letter["remaining_stock"] < 0 :
             letter["remaining_stock"] = 0
        last_sold_time = 0
        for goods in letter['goods']:
           if letter["flash_goods_id"] == goods["goodsId"]:
               last_sold_time = time.strftime("%H:%M",time.localtime(goods["last_sold_time"]/1000))
        stock_data["stock_" + str(letter["productId"])] = str(letter["remaining_stock"])+";"+str(last_sold_time)
    return stock_data
 
def product_info(request,productId):
    product_info_json = api_list.get_product_info_by_id(request,productId)
    return HttpResponse(json.dumps(product_info_json),content_type="application/json")



