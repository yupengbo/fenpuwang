# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from apps.api import api_list
from apps.utils import data_process_utils,string_utils, response_data_utils
import requests
import json
import cgi
import logging

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
    item_list_json = api_list.get_shopping_cart(request,'10E5C27B3AA37718CFF61A6CA32135196E4636F6500251D3801C302B9F68B58F')
    try:
        if item_list_json and item_list_json['error']==0:
            process_cartinfo_data(item_list_json)
            meta_data = {'cart_info_list':item_list_json['validCartItemList'],'invlid_cart_info_list':item_list_json['invalidCartItemList']}
            meta_data = response_data_utils.pack_data(request,meta_data)
            return render(request,'cart/cart.html',meta_data) 
    except Exception,e:
        print "===>" + str(e)
        return response_data_utils.error_response(request,None, __name__, e)

def set_contact(request):                                      
    num = request.REQUEST.getlist('num')
    total_num =request.REQUEST.get('total_fee')
    goods_ids = request.REQUEST.getlist('goods_id')
    print request.get_host()
    print request.get_full_path()
    print request.META
    print 222222222222222
    result = []
    for m in range(len(num)):
        result.append({'goodsId': goods_ids[m], 'num': num[m]})
    print result
    meta_data = {'cartInfo': json.dumps(result)}
    return render(request,'cart/setcontact.html',meta_data)
