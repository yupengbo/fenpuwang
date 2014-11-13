# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import json
import requests
from apps.api import api_list
from apps.utils import string_utils

def process_product_data(product_data):
  for question in product_data['questionList']:
    if question['relatedAnswer'] != None:
      question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content']) 
     
def question_list(request, product_id, mark):
  if request.is_ajax(): #仅接受ajax请求
    try:
      product_json = api_list.get_product_detail(product_id, 0, 20, mark)
      if product_json['error'] == 0:
        process_product_data(product_json)
        template = loader.get_template("lists/question_list.html")
        context = RequestContext(request, {'question_list':product_json['questionList']})
        next_request_url = reverse('product:question_list', kwargs = {"product_id":product_id, "mark":product_json['mark']})
        response_json = {'html':template.render(context), 'mark':product_json['mark'], 'url':next_request_url}
        return HttpResponse(json.dumps(response_json), content_type="application/json") 
    except Exception as e:
      print e
      return HttpResponse(e)
    raise Http404
  else:
    raise Http404
  
def product_detail(request, product_id):
  has_product_info = 1
  product_json = api_list.get_product_detail(product_id, has_product_info)
  try:
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return HttpResponse("product id invalid")
    process_product_data(product_json)
    next_request_url = reverse('product:question_list', kwargs ={"product_id":product_id, "mark":product_json['mark']})
    return render(request, 'product/product.html', {'product':product_json, 'url':next_request_url})
  except Exception,e:
    print e
    raise Http404
