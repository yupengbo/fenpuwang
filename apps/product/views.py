from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list
from apps.utils import string_utils

def truncate_text1(text, length = 200, suffix = "..."):
  if text == None:
    return None
  if len(text) > 200:
    text = text[0:200] + str(suffix)
  return text
  

def process_product_data(product_data):
  for question in product_data['questionList']:
    question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content']) 
  
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
