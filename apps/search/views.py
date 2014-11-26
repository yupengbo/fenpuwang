# -*- coding: utf-8 -*-

import string
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.utils.http import urlquote
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
import json
import requests
from apps.api import api_list
from apps.utils import string_utils, response_data_utils

def process_search_data(search_data):
  if search_data.get('questionList'):
    for question in search_data['questionList']:
      if question.get('relatedAnswer'):
        question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content'])
  if search_data.get('productList'):
    for product in search_data['productList']:
      pics = product.get('pics')
      if pics and len(pics) > 0:
        product['thumb_s'] = pics[0]['thumb-s']

def question_list(request, keyword, mark):
  if request.is_ajax() == False: #仅接受ajax请求
    raise Http404
  try:
    search_json = api_list.search(request, keyword, 2, 10, mark) 
    if search_json['error'] != 0:
      raise Http404 
    process_search_data(search_json)
    template = loader.get_template("lists/question_list.html")
    context = RequestContext(request, {'question_list':search_json['questionList']})
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    if search_json['mark'] == 0 or search_json['mark'] == "0":
      next_request_url = "" 
    response_json = {'html':template.render(context), 'mark':search_json['mark'], 'url':next_request_url}
    return HttpResponse(json.dumps(response_json), content_type="application/json") 
  except Exception as e:
    print e
    return HttpResponse(e)
    
def product_list(request, keyword, type, mark):
   is_ajax = request.is_ajax()
   try:
      search_result = api_list.search(request, keyword, 1, 10, mark)
      if search_result['error'] == 0 :
          process_search_data(search_result)
          next_request_url = ""
          if str(search_result['mark']) != "0":
              next_request_url = reverse('search:product_list', kwargs ={"type":type, "keyword":keyword,  "mark":search_result['mark']})
          meta_data = {'productList' : search_result["productList"], 'url':next_request_url, "keyword":keyword, 'from': 'search' }
          if is_ajax:
             context = RequestContext(request, meta_data)
             template = loader.get_template('products/product_effect_list.html')
             response_json = {'html':template.render(context), 'url':next_request_url}
             return HttpResponse(json.dumps(response_json), content_type="application/json")
          else:
             meta_data = response_data_utils.pack_data(request, meta_data)
             return render(request, 'products/products.html', meta_data)
   except Exception,e:
      print e
      raise Http404
   raise Http404


def search(request, keyword):
  search_json = api_list.search(request, keyword)
  try:
    print "xxxxxxxxxxxx"
    print search_json
    if search_json == None or search_json == "" or search_json['error'] != 0:
      return HttpResponse("search keyword invalid")
    process_search_data(search_json)
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    meta_data = response_data_utils.pack_data(request, {'search':search_json, 'url':next_request_url, 'keyword':keyword })
    return render(request, 'search/search.html', meta_data)
  except Exception,e:
    print e
    raise Http404
