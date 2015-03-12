# -*- coding: utf-8 -*-
from django.shortcuts import render
import string 
import logging
logger = logging.getLogger('django')

def pack_data(request,meta):
  referer = request.META.get('HTTP_REFERER')
  if meta:
    meta["closedownload"] = 0
    meta["close_bottom_download"] = 0
    if "closedownload" in request.COOKIES :
      value = request.COOKIES["closedownload"]
      if value == "1":
         meta["closedownload"] = 1
    bottom_key = u'bottom_download'
    if bottom_key in meta:
      if meta['bottom_download'] == '0':
        meta["close_bottom_download"] = 1 
    meta["device"] = get_user_device(request)
    meta["referer"] = referer
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

def error_response(request, message, view_name = "unknow_source", error_info = "unknow_error"):
  if not error_info:
     if message:
        error_info = message 
     else:
        error_info = "unkonw_error"
  if not message:
     message = "服务器忙，请稍后重试！"
  if not view_name:
     view_name = "unknow_source"
  view_name = view_name + ":"
  logger.error(view_name + str(error_info))
  return render(request, '500.html', {'text': message})

def error_log(request, message, view_name = "unknown_souurce", error_info="unkonw_error"):
  if not error_info:
     if message:
        error_info = message 
     else:
        error_info = "unkonw_error"
  if not message:
     message = "服务器忙，请稍后重试！"
  if not view_name:
     view_name = "unknow_source"
  view_name = view_name + ":"
  logger.error(view_name + str(error_info))

def error_comments(request, message, view_name = "unknown_souurce", error_info="unkonw_error"):
  error_log(request, message, view_name, error_info)


