# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import json
import requests
from apps.api import api_list
from apps.utils import string_utils, response_data_utils, weixin_auth_utils
import cgi

def process_product_data(product_data):  
  if product_data.get("contentList"):
    for content in product_data['contentList']:
        if content['type'] == 0:
            content['question']['title'] = string_utils.truncate_text2(content['question']['title'],36)

            if content['question']['relatedAnswer']!=None:     #答案有可能不存在
                content['question']['relatedAnswer']['content'] = string_utils.truncate_text(content['question']['relatedAnswer']['content'])   
        if content['type'] == 1:
            if content['featureTopic'] != None:
                content['featureTopic']['content'] = string_utils.truncate_text(content['featureTopic']['content'])
                content['featureTopic']['org'] = content['featureTopic']['pics'][0]['org']
            
                    

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
    return response_data_utils.error_response(request,"找不到问题列表！", __name__, "not ajax")
  try:
    product_json = api_list.get_related_question_by_product_id(request, product_id, mark)
    if product_json['error'] != 0:
      return response_data_utils.error_response(request,"找不到问题列表！", __name__, product_json)
    process_product_data(product_json)
    template = loader.get_template("lists/question_topic_list.html")
    context = RequestContext(request, {'question_topic_list':product_json['contentList']})
    next_request_url = reverse('product:question_list', kwargs = {"product_id":product_id, "mark":product_json['mark']})
    if product_json['mark'] == 0 or product_json['mark'] == "0":
      next_request_url = ""
    response_json = {'html':template.render(context), 'mark':product_json['mark'], 'url':next_request_url}
    return HttpResponse(json.dumps(response_json), content_type="application/json") 
  except Exception as e:
    return response_data_utils.error_response(request, "找不到问题列表！", __name__, e)
  
def product_detail(request, product_id):
  #微信中用户信息获取及授权处理
  dp = request.REQUEST.get('dp')
  user_info = weixin_auth_utils.get_user_info(request)
  authuri = user_info.get('redirect')
  session = user_info.get('session')

  user_agent = request.META.get('HTTP_USER_AGENT')

  is_mm = None
  user_agent = user_agent.lower()
  if "micromessenger" in user_agent:
    is_mm = 1

  if authuri and is_mm == 1 and dp != None and dp != "":
      return HttpResponseRedirect(authuri)
  from_user_name = None;
  if dp != "" and dp != None:
    api_list.bind_user(request, session, dp)
    from_user_info = api_list.get_user_info_by_uid(request, dp)
    if from_user_info != None:
      from_user_name = from_user_info.get("userInfo").get('userName')
  # end

  has_product_info = 1
  try:
    product_json = api_list.get_product_info_by_id(request, product_id)
    question_json = api_list.get_related_question_by_product_id(request, product_id, 0)
    cart_num_json = api_list.get_goods_num_in_cart(request, session)
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return response_data_utils.error_response(request, "找不到这个产品！",  __name__, product_json)
    product_json["mark"] = 0
    if question_json and question_json['error'] == 0 and question_json.get("contentList"):
      product_json["contentList"] = question_json["contentList"]
      product_json["mark"] = question_json["mark"]
      product_json["totalNumber"] = question_json["totalNumber"]

    product_json["cartNum"] = 0
    if cart_num_json and cart_num_json['error'] == 0:
      product_json["cartNum"] = cart_num_json["totalNum"]
    process_product_data(product_json)
    next_request_url = reverse('product:question_list', kwargs ={"product_id":product_id, "mark":product_json['mark']})
    meta = response_data_utils.pack_data(request, {'navTitle':'产品详情','product':product_json, 'url':next_request_url,'fromUserName':from_user_name})
    return weixin_auth_utils.fp_render(request,'product/product.html', meta, session)
  except Exception,e:
    print e
    return response_data_utils.error_response(request, "找不到这个产品！",  __name__, e, session)


def add_in_cart(request):
    goods_id = request.REQUEST.get('goodsId')
    product_id = request.REQUEST.get('productId')
    session = request.REQUEST.get('session')
    if not session:
        session = request.COOKIES.get("session")

    product_uri = 'http://m.fenpuwang.com/product/' + product_id + "/"
    authuri = weixin_auth_utils.build_auth_uri(product_uri)
    is_ajax = request.is_ajax()
    if not session:
        response_json = {'error': 2,"authuri":authuri}
        print response_json
        return HttpResponse(json.dumps(response_json), content_type="application/json")
    if not is_ajax:
        return response_data_utils.error_response(request, "非ajax!",  __name__, "no ajax")
    response_json = api_list.add_goods_in_cart(request,session, goods_id,product_id)
    #response_json = {'error': 0}
    print response_json
    return HttpResponse(json.dumps(response_json), content_type="application/json")

def del_in_cart(request):
    is_ajax = request.is_ajax()
    session = request.COOKIES.get("session")
    if not session:
        return response_data_utils.error_response(request, "invalid session!",  __name__, "invalid session")
    if not is_ajax:
        return response_data_utils.error_response(request, "非ajax!",  __name__, "no ajax")
    goods_id = request.REQUEST.get('goodsId')
    print api_list.delete_goods_in_cart(request,session, goods_id)
    response_json = {'error': 0}
    return HttpResponse(json.dumps(response_json), content_type="application/json")

def product_official(request, product_id):
  has_product_info = 1
  try:
    product_json = api_list.get_product_info_by_id(request, product_id)
    if product_json == None or product_json == "" or product_json['error'] != 0:
      return response_data_utils.error_response(request, "找不到这个产品的详情！", __name__ , product_json)
    process_product_link(product_json['product'])
    meta = response_data_utils.pack_data(request, {'product':product_json['product']})
    return render(request, 'product/product_official.html', meta) 
  except Exception,e:
    return response_data_utils.error_response(request, "找不到这个产品的详情！",  __name__, e) 

