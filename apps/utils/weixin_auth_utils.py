# -*- coding: utf-8 -*-
import string 
import json
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from urllib import urlencode
from apps.api import api_list
import datetime

appid = 'wxb37b8b2babf1f511'
app_secret = '9e289e06befd94ef1cf49f484ce9dd86'
base_uri = 'http://m.fenpuwang.com'

def url_encode(uri):
   data = {'': uri}
   uri = urlencode(data)
   return uri[1:]

def get_base_uri(request):
   return_uri = request.META.get("HTTP_HOST")
   if return_uri:
      return "http://"+return_uri
   return base_uri

 
def build_auth_uri(redirect_uri):
    redirect_uri = str(redirect_uri)
    redirect_uri = url_encode(redirect_uri)
    auth_uri = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect' % (appid, redirect_uri)
    return auth_uri

def get_user_info(request):
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

   code = None
   if not session:
      code = request.REQUEST.get("code")

   user_info = get_api_user_info(request, session, code) 
   session = user_info.get("session")
   if not session:
       return {'redirect':authuri}
   return user_info

def get_api_user_info(request, sessionKey, code):
  user_info = {}
  session = sessionKey
  if sessionKey:
     user_info = api_list.get_user_info(request, sessionKey)
  elif code:
     print "===>" + code
     user_info = api_list.check_login(request,code)

  if not user_info:
     return {}

  user_info=user_info.get("userInfo")
  if user_info:
      if user_info.get("sessionKey"):
          session = user_info.get("sessionKey")
      user_info["sessionKey"] = None
      user_info["session"] = session
      return user_info
  return {}

def fp_render(request, template_name,context,sessionKey):
   response  = render(request, template_name, context)
   if sessionKey:
      dt = datetime.datetime.now() + datetime.timedelta(hours = int(168))
      response.set_cookie('session',sessionKey,expires=dt)
   return response
