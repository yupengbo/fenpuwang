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

def water(request,activity_key):
    ticket = None
    ticket_info = {}
    base_uri = weixin_utils.get_base_uri(request)
    path_uri = reverse("activities:water",kwargs={})
    share_uri = base_uri + path_uri 
    ticket_info = api_list.get_js_ticket(request)
    if user_activity_info.get("ticket"):
        ticket = user_activity_info.get("ticket")
    meta_data = get_sign_info(request, ticket, self_uri)
    meta_data['appid'] = weixin_utils.get_appid()
    meta_data['base_uri'] = base_uri
    meta_data['share_uri'] = share_uri
    return render(request, 'activities/water' + activity_key +'.html', meta_data)


def get(request):
    return
def result(request):
    return
