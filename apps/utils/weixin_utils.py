# -*- coding: utf-8 -*-
import string 
import json
import requests
from django.http import HttpResponseRedirect
from urllib import urlencode

appid = 'wxb37b8b2babf1f511'
app_secret = '9e289e06befd94ef1cf49f484ce9dd86'

def get_appid():
   return appid

def url_encode(uri):
   data = {'': uri}
   uri = urlencode(data)
   return uri[1:]

def get_base_uri(request):
#   base_uri = request.META.get("HTTP_ORIGIN")
#   if not base_uri:
   base_uri = 'http://m.fenpuwang.com'
#   port = request.META.get("SERVER_PORT")
   #if port != '80':
   #   base_uri = base_uri + ":" + port 
   return base_uri

def code2token (code):
   api_uri = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (appid, app_secret, code)
   return api_uri
 
def get_userinfo_uri(access_token, openid):
   api_uri = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
   return api_uri

def build_error_response(errorString):
    return {'error':1,'errorString':errorString}

def build_auth_uri(redirect_uri):
    redirect_uri = str(redirect_uri)
    redirect_uri = url_encode(redirect_uri)
    auth_uri = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect' % (appid, redirect_uri)
    return auth_uri

def get_result(req, api_url, params):
    build_params(req,params)
    response = request('POST', api_url, params);
    result = build_error_response("server is busy-40331")
    try:
       if response.status_code == requests.codes.ok:
          result = response.json()
    except Exception,e:
       result = build_error_response("network anomaly-40332")
    return result

def request(method, api_name, params, time_out=30.0):
    api_str =  api_name
    print api_str
    print params
    return requests.request(method, api_str, data = params, timeout = time_out)

def build_params(req,params):
    if not params:
        params = {}
    if not req:
        return params
    return params

def get_user_info_by_code(req, code):
    result = {}
    token_info = get_result(req, code2token( code ), None )
    access_token = token_info.get('access_token')
    openid = token_info.get('openid')
    if not token_info or not access_token or not openid:
       return build_error_response("auth fail - 40333")

    user_info = get_result(req, get_userinfo_uri(access_token, openid ), {})
    unionid = user_info.get('unionid')
    nickname = user_info.get('nickname')
    headimgurl = user_info.get('headimgurl')
    if not user_info or not unionid:
        return build_error_response("auth fail - 40334")

    result['unionid'] = unionid
    result['nickname'] = nickname
    result['headimgurl'] = headimgurl
    result['openid'] = openid
    return result
