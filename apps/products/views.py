from django.shortcuts import render
from django.http import HttpResponse,Http404
from apps.api import api_list
import requests
from apps.utils import string_utils


from apps.api import api_list
# Create your views here.
def productlist_by_category(request, type=0,category_id=0,order=1,filter=0,mark=0):
    try:
        products_result = api_list.get_product_by_category(type, order, category_id, filter, 10, mark)
        if products_result['error'] == 0 :
            process_product_data(products_result)
            return render(request, 'products/products.html', {'products' : products_result})
    except Exception,e:
        print e
        raise Http404
    raise Http404

def process_product_data(product_data):
    for product in product_data['productList']:
        pics = product.get('pics')
        product['goodReviewRatio'] =  int(product['goodReviewRatio']*100)
        if pics and len(pics) > 0 :
            product['thumb_s'] = pics[0]['thumb-s']
