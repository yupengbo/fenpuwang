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
import logging
import cgi
logger = logging.getLogger('django')

def process_search_data(search_data):
  if search_data.get('questionList'):
    for question in search_data['questionList']:
      if question.get('relatedAnswer'):
        question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content'])
  if search_data.get('productList'):
    for product in search_data['productList']:
      effect = product.get('effect')
      if effect==None:
          product['effect'] = ""
      pics = product.get('pics')
      if pics and len(pics) > 0:
        product['thumb_s'] = pics[0]['thumb-s']
  if search_data.get('searchContentList'):
      for question_topic in search_data['searchContentList']:
          if question_topic['type'] == 0:
              question_topic['question']['title'] = cgi.escape(question_topic['question']['title'])
              question_topic['question']['title'] = string_utils.replace_newkeyword(question_topic['question']['title'])
              question_topic['question']['title'] = string_utils.replace_link(question_topic['question']['title'])
              if question_topic['question'].get('relatedAnswer'):
                  question_topic['question']['relatedAnswer']['content'] = cgi.escape(question_topic['question']['relatedAnswer']['content'])
                  question_topic['question']['relatedAnswer']['content'] = string_utils.replace_newkeyword(question_topic['question']['relatedAnswer']['content'])
                  question_topic['question']['relatedAnswer']['content'] = string_utils.truncate_text(string_utils.replace_link(question_topic['question']['relatedAnswer']['content']))
          if question_topic['type'] == 1:
              if question_topic['featureTopic']['title'] != None:
                question_topic['featureTopic']['title'] = cgi.escape(question_topic['featureTopic']['title'])
                question_topic['featureTopic']['title'] = string_utils.replace_newkeyword(question_topic['featureTopic']['title'])
                question_topic['featureTopic']['title'] = string_utils.replace_link(question_topic['featureTopic']['title'])
              else:
                question_topic['featureTopic']['title'] = ""
              question_topic['featureTopic']['content'] = cgi.escape(question_topic['featureTopic']['content'])
              question_topic['featureTopic']['content'] = string_utils.replace_newkeyword(question_topic['featureTopic']['content'])
              question_topic['featureTopic']['content'] = string_utils.truncate_text(string_utils.replace_link(question_topic['featureTopic']['content']))
      

def question_list(request, keyword, mark):
  if request.is_ajax() == False: #仅接受ajax请求
    return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__ , "not ajax") 
  try:
    search_json = api_list.search(request, keyword, 2, 10, mark) 
    if search_json['error'] != 0:
      return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, search_json)
    process_search_data(search_json)
    template = loader.get_template("lists/question_topic_list.html")
    context = RequestContext(request, {'question_topic_list':search_json['searchContentList']})
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    if search_json['mark'] == 0 or search_json['mark'] == "0":
      next_request_url = "" 
    response_json = {'html':template.render(context), 'mark':search_json['mark'], 'url':next_request_url}
    return HttpResponse(json.dumps(response_json), content_type="application/json") 
  except Exception as e:
    return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)


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
     return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)

def search(request, keyword):
  search_json = api_list.search(request, keyword)
  try:
    if search_json == None or search_json == "" or search_json['error'] != 0:
      return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, search_json)
    process_search_data(search_json)
    next_request_url = reverse('search:question_list', kwargs = {"keyword":keyword, "mark":search_json['mark']})
    meta_data = response_data_utils.pack_data(request, {'search':search_json, 'url':next_request_url, 'keyword':keyword })
    return render(request, 'search/search.html', meta_data)
  except Exception,e:
    return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)


    
  





