from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list
from apps.utils import string_utils

def process_product_data(product_data):
  for question in product_data['questionList']:
    question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content']) 
  for pic in product_data['product']['pics']:
    pic['thumb_b'] = pic['thumb-b']
    pic['thumb_s'] = pic['thumb-s']
    pic['thumb_l'] = pic['thumb-l']
     
  
def product_detail(request, product_id):
  has_product_info =  1
  product_json = api_list.get_product_detail(product_id, has_product_info)
  try:
    if product_json == None or product_json == "":
      return HttpResponse("product id invalid")
    process_product_data(product_json)
    return render(request, 'product/product.html', {'product':product_json})
  except Exception,e:
    print e
    raise Http404
