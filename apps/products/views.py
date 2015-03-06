# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from apps.api import api_list
import requests
from apps.utils import string_utils, response_data_utils
from apps.api import api_list, static_data
from django.core.urlresolvers import reverse
import json
import logging

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

def products_recommend(request):                                                        #kim 
    products_promote_result = api_list.get_promote_product_list(request)
    products_feature_result = api_list.get_feature_product_list(request)
    if not products_promote_result or products_promote_result['error']==1:
        return response_data_utils.error_response(request, "主推产品不存在！",__name__, products_promote_result)
    if ( not products_feature_result ) or products_feature_result['error']!=0:
        return response_data_utils.error_response(request,"推荐产品不存在",__name__,products_feature_result)
    try: 
        process_products_promote(products_promote_result)
        process_products_feature(products_feature_result)
        next_request_url = ""
        if str(products_feature_result['mark']) != "0":
           next_request_url = reverse('products:products_recommend_list', kwargs ={"mark":products_feature_result['mark']})
        
        meta_data = {'url':next_request_url, 'nav':'products',"products_promote_list":products_promote_result.get('productList'),"products_feature_list":products_feature_result.get('productList')}
        meta_data = response_data_utils.pack_data(request, meta_data)
        return render(request,'products/products_recommend.html',meta_data)
    except Exception,e:
        return response_data_utils.error_response(request, "推荐产品不存在！",__name__, e)

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
