# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
import requests
from apps.utils import data_process_utils, response_data_utils, string_utils
import json
from django.core.urlresolvers import reverse
# Create your views here.


def signup(request):
   if request.is_ajax(): #仅接受ajax请求
      response_json = {'error':1 ,'content': u"无效的验证码"};
      return HttpResponse(json.dumps(response_json), content_type="application/json")
   else:
      return render(request, 'ucenter/signup.html')

def change(request):
      sessionKey = request.META.get("HTTP_SESSIONKEY")
      if not sessionKey:
           sessionKey = request.REQUEST.get("sessionKey")
      if not sessionKey:
           return response_data_utils.error_response(request, None,  __name__, " not find sessionKey")
      return render(request, 'ucenter/change.html', {'sessionKey': sessionKey})

def sendCode(request):
   if request.is_ajax(): #仅接受ajax请求
       try:
          response_json = {'error':0}
          return HttpResponse(json.dumps(response_json), content_type="application/json")
       except Exception as e:
          return response_data_utils.error_response(request, None, __name__, e)
   return response_data_utils.error_response(request, None,  __name__, " not ajax")
