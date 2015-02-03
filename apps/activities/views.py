# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404,HttpResponseRedirect
import requests
from apps.utils import data_process_utils, response_data_utils, string_utils
import json
import time
from apps.api import api_list
from apps.utils import weixin_utils
from apps.utils.sign import Sign
from django.core.urlresolvers import reverse
# Create your views here.

def get_view_uid(request):
    view_uid = 0 
    if request.REQUEST.get("fromuid"):
        view_uid = request.REQUEST.get("fromuid")
    return view_uid

def get_request_from(request):
    request_from = 'timeline'
    if request.REQUEST.get("from"):
        request_from = request.REQUEST.get("from")
    return request_from

def get_sign_info(request, ticket, self_uri):
    meta_data = {}
    if ticket:
        sign = Sign(ticket, self_uri)
        meta_data = sign.sign()

    if not meta_data.get('timestamp'):
        meta_data['timestamp'] = 0

    if not meta_data.get('nonceStr'):
       meta_data['nonceStr'] = "" 

    if not meta_data.get('signature'):
       meta_data['signature'] = "" 

    return meta_data

def activity(request, activity_id):
    session = None
    session = request.COOKIES.get("session")
    ticket = None
    user_activity_info = {}
    user_info = {}
    
    view_uid = get_view_uid(request)
    request_from = get_request_from(request)
    base_uri = weixin_utils.get_base_uri(request)
    self_uri = reverse("activities:activity",kwargs={'activity_id': activity_id})
    query_str = request.META['QUERY_STRING']
    if query_str and len(query_str)>0:
       query_str = "?" + query_str
    else:
       query_str = ''
    self_uri = share_uri + query_str
    
    authuri = weixin_utils.build_auth_uri(self_uri)
    if not session:
       code = request.REQUEST.get("code")
       user_info = {}
       if code:
           user_info = api_list.check_login(request,code)
           if user_info:
              user_info=user_info.get("userInfo")
           if user_info:
              session = user_info.get("sessionKey")

    if not session:
        return HttpResponseRedirect(authuri)

    if session: 
        user_activity_info = api_list.get_activity_info(request, session, activity_id, view_uid)

    if user_activity_info.get("error") == None or str(user_activity_info["error"]) != "0":
        user_activity_info["shareActivity"] = 0
        user_activity_info["bonus"] = 0
    else:
        ticket = user_activity_info.get("ticket")

    user_uid = user_activity_info.get("uID")
    if not user_uid:
        user_uid = 0
    share_uri = base_uri + self_uri + "?fromuid=" + user_uid

    meta_data = get_sign_info(request, ticket, self_uri)
    meta_data['session'] = session
    meta_data['appid'] = weixin_utils.get_appid()
    meta_data['share_activity_fee'] = user_activity_info.get("shareActivity")
    meta_data['bonus_fee'] = user_activity_info.get("bonus")
    meta_data['nickName'] = user_activity_info.get("nickName")
    if not meta_data.get('nickName'):
       meta_data['nickName'] = '粉扑'
    if not meta_data.get('avatarURL'):
       meta_data['avatarURL'] = 'http://dabanniu.oss.aliyuncs.com/img_user_avatars_default@2x.png'
    meta_data['avatarURL'] = user_activity_info.get("avatarURL")
    meta_data['total_fee'] = meta_data['bonus_fee'] + meta_data['share_activity_fee']
    meta_data['view'] = 'share_bonus'
    if request_from == 'weixin' :
        if  meta_data['share_activity_fee'] >0 :
            meta_data['view'] = 'view_result'
        else:
            meta_data['view'] = 'share_bonus'
    else:
        if  meta_data['share_activity_fee'] >0 and meta_data['bonus_fee'] > 0:
            meta_data['view'] = 'view_result'
        elif meta_data['bonus_fee'] == 0 :
            meta_data['view'] = 'open_bonus'
        else:
            meta_data['view'] = 'opened'
    meta_data['base_uri'] = base_uri
    meta_data['request_from'] = request_from 
    meta_data['activity_id'] = activity_id
    meta_data['share_uri'] = share_uri
    response_data_utils.pack_data(request,meta_data)
    return render(request, 'activities/activity.html', meta_data) 

def share_activity(request, activity_id):
    is_ajax = request.is_ajax()
    session = request.REQUEST.get("session")
    if not session:
        session = request.COOKIES.get("session")
    if session:
        result = api_list.user_share_log(request, session, activity_id, 10, 1)
        response_json = json.dumps(result)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 


def open_bonus(request, activity_id):
    is_ajax = request.is_ajax()
    session = request.REQUEST.get("session")
    if not session:
        session = request.COOKIES.get("session")
    if is_ajax and session:
        result = api_list.open_bonus(request, session, activity_id)
        response_json = json.dumps(result)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 

