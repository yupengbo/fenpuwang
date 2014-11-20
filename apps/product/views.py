# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import json
import requests
from apps.api import api_list
from apps.utils import string_utils
import cgi

def process_product_data(product_data):
  for question in product_data['questionList']:
    if question['relatedAnswer'] != None:
      question['relatedAnswer']['content'] = string_utils.truncate_text(question['relatedAnswer']['content']) 

def process_product_link(product_data):
  details = product_data.get("details")
  if details:
    product_data["details"] = string_utils.replace_text_newline(cgi.escape(details))
  for link in product_data['mapping']:
    # 官方
    if link['webId'] == "0" or link['webId'] == 0:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_web.png"
    #聚美
    if link['webId'] == "2" or link['webId'] == 2:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_jumei.png"
    #乐蜂
    if link['webId'] == "3" or link['webId'] == 3:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_lefeng.png"
    #丝芙兰
    if link['webId'] == "4" or link['webId'] == 4:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_sephora.png"
    #天猫
    if link['webId'] == "5" or link['webId'] == 5:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_tmall.png"
    #京东
    if link['webId'] == "6" or link['webId'] == 6:
      link['logo_img'] = "/static/images/icon_prduct_jieshao_jd.png"

def question_list(request, product_id, mark):
  if request.is_ajax() == False: #仅接受ajax请求
    raise Http404

  try:
    product_json = api_list.get_product_detail(product_id, 0, 20, mark)
    if product_json['error'] != 0:
      raise Http404
    process_product_data(product_json)
    template = loader.get_template("lists/question_list.html")
    context = RequestContext(request, {'question_list':product_json['questionList']})
    next_request_url = reverse('product:question_list', kwargs = {"product_id":product_id, "mark":product_json['mark']})
    if product_json['mark'] == 0 or product_json['mark'] == "0":
      next_request_url = ""
    response_json = {'html':template.render(context), 'mark':product_json['mark'], 'url':next_request_url}
    return HttpResponse(json.dumps(response_json), content_type="application/json") 
  except Exception as e:
    print e
    return HttpResponse(e)
  
def product_detail(request, product_id):
  has_product_info = 1
  product_json = api_list.get_product_detail(product_id, has_product_info)
  try:
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return HttpResponse("product id invalid")
    process_product_data(product_json)
    next_request_url = reverse('product:question_list', kwargs ={"product_id":product_id, "mark":product_json['mark']})
    return render(request, 'product/product.html', {'product':product_json, 'url':next_request_url})
  except Exception,e:
    print e
    raise Http404

def product_official(request, product_id):
  has_product_info = 1
  product_json = api_list.get_product_detail(product_id, has_product_info)
  try:
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return HttpResponse("product id invalid")
    process_product_link(product_json['product'])
    return render(request, 'product/product_official.html', {'product':product_json['product']})
  except Exception,e:
    print e
    raise Http404

