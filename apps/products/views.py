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
# Create your views here.
def productlist_by_category(request, type=0,category_id=0,order=1,filter=0,mark=0):
    is_ajax = request.is_ajax()
    try:
        products_result = api_list.get_product_by_category(request, type, order, category_id, filter, 10, mark)
        if products_result['error'] == 0 :
            process_product_data(products_result)
            next_request_url = ""
            if str(products_result['mark']) != "0":
                next_request_url = reverse('products:queryt_by_all', kwargs ={"type":type, "category_id":category_id, "order":order, "filter":filter, "mark":products_result['mark']})
            meta_data = {'productList' : products_result["productList"], 'url':next_request_url ,'nav':'products'}
            if is_ajax:
                context = RequestContext(request, meta_data)
                template = loader.get_template('products/product_list.html')
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                meta_data = dict(meta_data.items() + {"type":type, "category_id":category_id, "order":order, "filter":filter}.items())
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
