# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
import requests
from apps.utils import data_process_utils, response_data_utils, string_utils
import json
import time
from apps.api import api_list
from apps.utils import weixin_utils
from django.core.urlresolvers import reverse
# Create your views here.

def get_request_from(request):
    request_from = 'timeline'
    if request.REQUEST.get("from"):
        request_from = request.REQUEST.get("from")
    return request_from


def activity(request, activity_id):
    session = request.COOKIES.get("session")
    print request.COOKIES
    user_activity_info = {}
    user_info = {}
    if not session:
       code = request.REQUEST.get("code")
       print code
       user_info = {}
       if code:
           #user_info = weixin_utils.get_user_info_by_code(request,code)
           user_info = api_list.check_login(request,code)
           if user_info:
              user_info=user_info.get("userInfo")
           if user_info:
              session = user_info.get("sessionKey")

    print user_info

    meta_data = {}
    if session: 
        print "=================>" + session
        user_activity_info = api_list.get_activity_info(request, session, activity_id)
        print user_activity_info
        meta_data['session'] = session

    meta_data['share_activity_fee'] = user_activity_info.get("shareActivity")
    meta_data['bonus_fee'] = user_activity_info.get("bonus")
    meta_data['request_from'] = get_request_from(request) 
    meta_data['activity_id'] = activity_id
    #获取用户信息
    print meta_data
    return render(request, 'activities/activity.html', meta_data) 

def wx_auth(request, activity_id):
    is_ajax = request.is_ajax()
    if is_ajax:
        request_from = get_request_from(request)
        base_uri = weixin_utils.get_base_uri(request)
        redirect_uri = reverse("activities:activity",kwargs={'activity_id': activity_id}) + "?from=" + request_from 
        authuri = weixin_utils.build_auth_uri(base_uri + str(redirect_uri))
        response_json = { 'uri' : authuri }
        response_json = json.dumps(response_json)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 

def share_activity(request, activity_id):
    is_ajax = request.is_ajax()
    session = request.COOKIES.get("session")
    if is_ajax and session:
        result = api_list.share_activity(request, session, activity_id, 10, 1)
        response_json = json.dumps(result)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 


def open_bonus(request, activity_id):
    is_ajax = request.is_ajax()
    session = request.COOKIES.get("session")
    print request.COOKIES
    print session
    if is_ajax and session:
        result = api_list.open_bonus(request, session, activity_id)
        print result
        response_json = json.dumps(result)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 

