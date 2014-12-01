# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import json
import requests
from apps.api import api_list
from apps.utils import string_utils, response_data_utils
import cgi

def process_product_data(product_data):
  if product_data.get("questionList"):
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
    product_json = api_list.get_related_question_by_product_id(request, product_id, mark)
    if product_json['error'] != 0:
      return render(request, '500.html', {'text': "找不到问题列表！"})
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
    return render(request, '500.html', {'text': "找不到问题列表！"})
  
def product_detail(request, product_id):
  has_product_info = 1
  try:
    product_json = api_list.get_product_info_by_id(request, product_id)
    question_json = api_list.get_related_question_by_product_id(request, product_id, 0)
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return render(request, '500.html', {'text': "找不到这个产品！"})
    if question_json and question_json['error'] == 0 and question_json.get("questionList"):
      product_json["questionList"] = question_json["questionList"]
      product_json["mark"] = question_json["mark"]
      product_json["totalNumber"] = question_json["totalNumber"]
    process_product_data(product_json)
    next_request_url = reverse('product:question_list', kwargs ={"product_id":product_id, "mark":product_json['mark']})
    meta = response_data_utils.pack_data(request, {'product':product_json, 'url':next_request_url})
    return render(request, 'product/product.html', meta)
  except Exception,e:
    print e
    raise Http404

def product_official(request, product_id):
  has_product_info = 1
  try:
    product_json = api_list.get_product_info_by_id(request, product_id)
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return HttpResponse("product id invalid")
    process_product_link(product_json['product'])
    meta = response_data_utils.pack_data(request, {'product':product_json['product']})
    return render(request, 'product/product_official.html', meta) 
  except Exception,e:
    print e
    raise Http404

