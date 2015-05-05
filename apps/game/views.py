# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404,HttpResponseRedirect
import requests
from apps.utils import data_process_utils, response_data_utils, string_utils,weixin_auth_utils
import json
import time
from apps.api import api_list
from apps.utils import weixin_utils
from apps.utils.sign import Sign
from django.core.urlresolvers import reverse
import datetime
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

def makeup(request, activity_key):
    session = request.COOKIES.get("session")
    score = request.COOKIES.get("show_score")
    show_result = request.COOKIES.get("show_result")
    code = request.REQUEST.get("code")
    user_agent = request.META.get('HTTP_USER_AGENT')
    is_mm = None
    user_agent = user_agent.lower()
    if "micromessenger" in user_agent:
        is_mm = 1

    if request.REQUEST.get('c') == '1' :
       response = render(request, 'game/makeup.html', {"is_mm": is_mm})
       clean_cookie(response)
       return response

    if not session:
        session = request.REQUEST.get("session")
        print session

    if not session:
        code = request.REQUEST.get("code")
        print code

    user_info = {}
    if code:
        user_info = api_list.check_login(request,code)
        if user_info:
            user_info=user_info.get("userInfo")
        if user_info:
            session = user_info.get("sessionKey")

    print session
    print score

    result = {}
    if session and score:
        result = api_list.get_game_result(request, session, score)
    
    print result
    if not result:
        result = {}
    result["is_mm"] = is_mm
    response = render(request, 'game/makeup.html', result)
    return write_show_result_cookie(response, 0 , score, session) 


def get(request):
    #response  = HttpResponse("{\"error\":0}",content_type="application/json")
    #return response
    is_ajax = request.is_ajax()
    session = request.REQUEST.get("session")
    if not session:
        session = request.COOKIES.get("session")
    score = request.REQUEST.get("score")
    if not score:
       return HttpResponse("{\"error\":1,\"errorString\":\"没有积分\"}",content_type="application/json")

    game_uri = 'http://m.fenpuwang.com/game/makeup/1/?score=' + str(score)
    authuri = weixin_auth_utils.build_auth_uri(game_uri)
    is_ajax = request.is_ajax()
    if not session:
        response_json = {'error': 2,"authuri":authuri}
        print response_json
        response = HttpResponse(json.dumps(response_json), content_type="application/json")
        return write_show_result_cookie(response, 1 , score);

    if is_ajax and session:
        result = api_list.get_game_result(request, session, score)
        response_json = json.dumps(result)
        return HttpResponse(response_json,content_type="application/json")
    else:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax") 

def write_show_result_cookie(response, show, score, session = None):
    dt = datetime.datetime.now() + datetime.timedelta(hours = int(168000))
    if show:
        response.set_cookie('show_result', show , expires=dt)
    if score:
        response.set_cookie('show_score', score , expires=dt)
    if session:
        response.set_cookie('session', session , expires=dt)
    return response

def clean_cookie(response):
    response.set_cookie('show_result', '' , expires=0)
    response.set_cookie('show_score', '', expires=0)
    response.set_cookie('session', '', expires=0)
