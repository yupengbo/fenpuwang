# -*- coding: utf-8 -*-
import string 

def pack_data(request,meta):
  if meta:
    meta["closedownload"] = 0
    if "closedownload" in request.COOKIES :
      value = request.COOKIES["closedownload"]
      if value == "1":
         meta["closedownload"] = 1
    meta["device"] = get_user_device(request)
  return meta

def get_user_device(request):
  device = 'pc'
  if 'HTTP_USER_AGENT' in request.META :
    http_user_agent = request.META['HTTP_USER_AGENT']
    http_user_agent = http_user_agent.lower()
    if 'iphone' in http_user_agent or 'ipad' in http_user_agent or 'ipod' in http_user_agent or 'ios' in http_user_agent :
      device = 'ios'
    elif 'android' in http_user_agent :
      device = 'android'
  return device
