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
    #return render(request,'cart/cart.html',{})
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri:
        return HttpResponseRedirect(authuri)
    item_list_json = api_list.get_shopping_cart(request,session)
    try:
        if item_list_json and item_list_json['error']==0:
            process_cartinfo_data(item_list_json)
            meta_data = {'search_btn':1,'navTitle':'购物车', 'cart_info_list':item_list_json['validCartItemList'],'invalid_cart_info_list':item_list_json['invalidCartItemList']}
            if len(item_list_json['validCartItemList']) == 0 and len(item_list_json['invalidCartItemList']) == 0:
                return response_data_utils.error_response(request,"您的购物车空空如也", __name__, "购物车为空")
            meta_data = response_data_utils.pack_data(request,meta_data)
            return weixin_auth_utils.fp_render(request,'cart/cart.html',meta_data, session) 
    except Exception,e:
        return response_data_utils.error_response(request,None, __name__, e, session)

def set_contact(request):                                      
    is_mm = 0
    if request.META.get('HTTP_USER_AGENT').lower().find("micromessenger") != -1:
      is_mm = 1

    #return render(request,'cart/setcontact.html',{})
    user_info = weixin_auth_utils.get_user_info(request)
    authuri = user_info.get('redirect')
    session = user_info.get('session')
    if authuri and is_mm == 1:
        return HttpResponseRedirect(authuri)
    num = request.REQUEST.getlist('num')
    total_num =request.REQUEST.get('total_fee')
    goods_ids = request.REQUEST.getlist('goods_id')
    orderId = request.REQUEST.get('orderId')
    if not total_num:
        return response_data_utils.error_response(request,"非法请求", __name__, "非法请求", session)
    readonly = None

    if orderId:
      readonly = 1
    else:
      orderId = ''
    result = []
    for m in range(len(num)):
        result.append({'goodsId': goods_ids[m], 'num': num[m]})
    cartInfo = json.dumps(result)
    api_list.update_shopping_cart(request,session,cartInfo)
    meta_data = {'search_btn':1,'cartInfo': cartInfo,'contact': clean_none(user_info.get("contact")),'orderId': orderId, 'readonly': readonly, \
	'address': clean_none(user_info.get("address")),'contactPhone': clean_none(user_info.get("contactPhone")),\
	'total_num': total_num,'navTitle':'支付','wxpayShow':is_mm}
    return weixin_auth_utils.fp_render(request,'cart/setcontact.html',meta_data, session) 

def clean_none(s):
   if not s:
      return ""
   return s

