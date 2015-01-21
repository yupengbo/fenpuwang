# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
import requests
from apps.utils import data_process_utils, response_data_utils, string_utils
import json
from apps.api import api_list
from django.core.urlresolvers import reverse
# Create your views here.


def signup(request):
   if request.is_ajax(): #仅接受ajax请求
      response_json = {'error':1 ,'content': u"无效的验证码"};
      return HttpResponse(json.dumps(response_json), content_type="application/json")
   else:
      return render(request, 'ucenter/signup.html')

def process_log_data(logs):
   if logs:
      for log in logs:
          log['creationTime'] = data_process_utils.get_time_since(log['creationTime'])       

def change(request, sessionKey = '', mark = 0):
    is_ajax = request.is_ajax()
    if not is_ajax:
       sessionKey = request.META.get("HTTP_SESSIONKEY")
    if not sessionKey:
       sessionKey = request.REQUEST.get("sessionKey")
    if not sessionKey:
       return response_data_utils.error_response(request, None,  __name__, " not find sessionKey")
    try:
        change_info = None
        if not is_ajax:
            change_info = api_list.get_user_change_info(request, sessionKey)
        logs = api_list.get_user_change_log(request, sessionKey, mark)
        if logs['error'] == 0:
           next_page_url = ''  # for next page ajax loading
           if int(logs['mark']) > 0:
               next_page_url = reverse('ucenter:change_log_list', kwargs ={"sessionKey": sessionKey, "mark": logs['mark']})
           process_log_data(logs["userChangeLogList"])
           meta_data = {'change_info' : change_info,'userChangeLogList' : logs["userChangeLogList"], 'url':next_page_url}
           if is_ajax:
              context = RequestContext(request, meta_data)
              template = loader.get_template('ucenter/change_log_list.html')
              response_json = {'html':template.render(context), 'url':next_page_url}
              return HttpResponse(json.dumps(response_json), content_type="application/json")
           else:
              meta_data = response_data_utils.pack_data(request, meta_data)
              return render(request, 'ucenter/change.html', meta_data)
        else:
           return response_data_utils.error_response(request, "找不到这个页面！",  __name__, logs)
    except Exception as e:
        return response_data_utils.error_response(request,"找不到这个页面！", __name__, e)

def sendCode(request):
   if request.is_ajax(): #仅接受ajax请求
       try:
          response_json = {'error':0}
          return HttpResponse(json.dumps(response_json), content_type="application/json")
       except Exception as e:
          return response_data_utils.error_response(request, None, __name__, e)
   return response_data_utils.error_response(request, None,  __name__, " not ajax")
