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
from apps.utils import string_utils

def process_search_data(search_data):
  for question in search_data['questionList']:
    question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content']) 
  for product in search_data['productList']:
    pics = product.get('pics')
    if pics and len(pics) > 0:
      product['thumb_s'] = pics[0]['thumb-s']

def question_list(request, keyword, mark):
  print "=++++++++++++++++"
  if request.is_ajax() == False: #仅接受ajax请求
    raise Http404
  try:
    search_json = api_list.search(keyword, 0, 20, mark) 
    if search_json['error'] != 0:
      return
    process_search_data(search_json)
    template = loader.get_template("lists/question_list.html")
    context = RequestContext(request, {'question_list':search_json['questionList']})
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    response_json = {'html':template.render(context), 'mark':search_json['mark'], 'url':next_request_url}
    return HttpResponse(json.dumps(response_json), content_type="application/json") 
  except Exception as e:
    print e
    return HttpResponse(e)
    
  
def search(request, keyword):
  search_json = api_list.search(keyword)
  try:
    if search_json == None or search_json == "" or search_json['error'] != 0:
      return HttpResponse("search keyword invalid")
    process_search_data(search_json)
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    return render(request, 'search/search.html', {'search':search_json, 'url':next_request_url})
  except Exception,e:
    print e
    raise Http404
