#coding:UTF-8
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
import time

logger = logging.getLogger('django')

def order_list(request):                                                         #kim                                     
    order_list_result = api_list.list_my_product_order(request)          
    if not order_list_result or order_list_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_list_result)    
    try:
        meta_data = {"order_list":order_list_result["productOrderList"]}
        return render(request,"order/orders.html",meta_data)
    except Exception,e:
        print e
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__, e)


def order_detail(request,order_id):                                            #kim
    order_detail_result = api_list.get_product_order(request,order_id)
   # cart_num = api_list.get_goods_num_in_cart(request)
    if not order_detail_result or order_detail_result["error"]!=0:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！",__name__,order_detail_result)
    try:
        process_order_detail(order_detail_result)
        meta_data = {"order":order_detail_result}
        return render(request,"order/order.html",meta_data)
    except Exception,e:
        print e
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)

def process_order_detail(data):
    if data["productOrder"].get("creationTime"):
        time_tuple = time.localtime(data["productOrder"]["creationTime"]/1000)
        data["productOrder"]["creationTime"] =  time.strftime("%Y-%m-%d %H:%M",time_tuple)

     
