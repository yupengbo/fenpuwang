# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from apps.api import api_list
from apps.utils import data_process_utils, string_utils, response_data_utils, weixin_auth_utils
import requests
import json
import cgi
import logging
import time
import codecs
import md5

logger = logging.getLogger('django')
def process_cartinfo_data(cart_info_data):
    if cart_info_data.get('validCartItemList'):
        process_itemlist_data(cart_info_data.get('validCartItemList'))
        cart_info_data
    if cart_info_data.get('invalidCartItemList'):
        process_itemlist_data(cart_info_data.get('invalidCartItemList'))

def process_itemlist_data(cart_item_list_data):
      for cart_item in cart_item_list_data:
          product = cart_item.get('product')
          if product:
              pics = product.get('pics')
              if pics and len(pics) > 0 :
                   product['thumb_s'] = pics[0]['thumb-s']


def cart_index(request):
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return HttpResponseRedirect(authuri)
    item_list_json = api_list.get_shopping_cart(request,session)
    try:
        if item_list_json and item_list_json['error']==0:
            process_cartinfo_data(item_list_json)
            meta_data = {'cart_info_list':item_list_json['validCartItemList'],'invlid_cart_info_list':item_list_json['invalidCartItemList']}
            meta_data = response_data_utils.pack_data(request,meta_data)
            return weixin_auth_utils.fp_render(request,'cart/cart.html',meta_data, session) 
    except Exception,e:
        return response_data_utils.error_response(request,None, __name__, e)

def set_contact(request):                                      
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return HttpResponseRedirect(authuri)
    num = request.REQUEST.getlist('num')
    total_num =request.REQUEST.get('total_fee')
    goods_ids = request.REQUEST.getlist('goods_id')
    result = []
    for m in range(len(num)):
        result.append({'goodsId': goods_ids[m], 'num': num[m]})
    cartInfo = json.dumps(result)
    api_list.update_shopping_cart(request, cartInfo, session)
    meta_data = {'cartInfo': cartInfo}
    return render(request,'cart/setcontact.html',meta_data)

# 传入参数:中文需要gbk编码
# 订单id
#
#
def order_pay(request) :
    agent_bill_id = request.REQUEST.get("order_id") 
    pay_amt = request.REQUEST.get("total_fee") 
    pay_code = request.REQUEST.get("bank_type") 
    goods_num = request.REQUEST.get("goods_num") 
    user_ip = "114_243_214_122"

    version = "1"
    agent_id = "1956513"  #汇付宝商户id
    key = "1A5D243267734BD68DB904EA" #商户秘钥
    agent_bill_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    pay_type = "20" 
    notify_url = "http://www.baidu.com"
    return_url = "http://www.baidu.com"
    goods_name = "0000"
    goods_note = ""
    remark = ""

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
    print sign_str
    print agent_bill_time
    
    sign = string_utils.get_md5(sign_str)
    meta_data = {'version':version, 'agent_id':agent_id, 'agent_bill_id':agent_bill_id,
                  'agent_bill_time':agent_bill_time, 'pay_type':pay_type, 'pay_code':pay_code,
                  'pay_amt':pay_amt, 'notify_url':notify_url, 'return_url':return_url,
                  'user_ip':user_ip, 'goods_name':goods_name, 'goods_num':goods_num,
                  'goods_note':goods_note, "remark":remark, "sign":sign}

    return render(request, 'cart/order_pay.html', meta_data)

