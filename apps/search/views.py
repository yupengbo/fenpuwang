# -*- coding: utf-8 -*-

import string
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.utils.http import urlquote
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

def search(request, keyword):
  search_json = api_list.search(keyword)
  try:
    if search_json == None or search_json == "":
      return HttpResponse("search keyword invalid")
    process_search_data(search_json)
    print search_json
    return render(request, 'search/search.html', {'search':search_json})
  except Exception,e:
    print e
    raise Http404
