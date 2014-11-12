# -*- coding: utf-8 -*-

import string
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.utils.http import urlquote
import requests
from apps.api import api_list
from apps.utils import string_utils

def search(request, keyword):
  search_json = api_list.search(keyword)
  try:
    if search_json == None or search_json == "":
      return HttpResponse("search keyword invalid")
    return render(request, 'search/search.html', {'search':search_json})
  except Exception,e:
    print e
    raise Http404
