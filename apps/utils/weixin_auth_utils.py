# -*- coding: utf-8 -*-
import string 
import json
import requests
from django.http import HttpResponseRedirect
from urllib import urlencode
from apps.api import api_list

appid = 'wxb37b8b2babf1f511'
app_secret = '9e289e06befd94ef1cf49f484ce9dd86'
base_uri = 'http://wxtest.fenpuwang.com'

def url_encode(uri):
   data = {'': uri}
   uri = urlencode(data)
   return uri[1:]

def get_base_uri(request):
   return base_uri

 
def build_auth_uri(redirect_uri):
    redirect_uri = str(redirect_uri)
    redirect_uri = url_encode(redirect_uri)
    auth_uri = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect' % (appid, redirect_uri)
    return auth_uri

def get_session_key(request):
   session = None
   session = request.COOKIES.get("session")
   if not session:
      session = request.REQUEST.get("session")
   host = get_base_uri(request)
   path_uri = request.META.get('PATH_INFO')
   query_str = request.META['QUERY_STRING']
   if query_str and len(query_str)>0:
      query_str = "?" + query_str
   else:
      query_str = ''

   self_uri = host + path_uri + query_str

   authuri = build_auth_uri(self_uri)

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
      user_info = api_list.get_user_info(request, session)
