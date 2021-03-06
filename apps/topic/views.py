# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from apps.api import api_list
import requests
from apps.utils import string_utils, response_data_utils, data_process_utils, weixin_auth_utils
from apps.api import api_list, static_data
from django.core.urlresolvers import reverse
import json
import time
import cgi
import logging

logger = logging.getLogger('django')
def topic_info(request, topic_id):
    dp = request.REQUEST.get('dp')
    #微信中用户信息获取及授权处理
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
    try:
        topic_json = api_list.get_feature_topic_info(request, topic_id)
        if topic_json == None or topic_json == "" or topic_json['error'] != 0:
          return response_data_utils.error_response(request,"找不到这个专题", __name__, topic_json, session)
        uid = request.GET.get('dp')
        bottom_download = request.GET.get('bottom_download')
        process_topic_data(topic_json)
        process_topic_url(uid, topic_json)
        topic_comments_json = topic_comments(request,topic_id)
        next_page_url = reverse("topic:topic_info_comments",kwargs={"topic_id":topic_id,"mark":topic_comments_json["mark"]})
        meta = response_data_utils.pack_data(request, {'featureTopic': topic_json['featureTopic'],'commentsTopic':topic_comments_json,'nav':'topic','navTitle':'笔记详情','bottom_download':bottom_download, 'fromUserName':from_user_name,'url':next_page_url})
        return weixin_auth_utils.fp_render(request,'topic/topic.html', meta, session)
    except Exception,e:
       return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e, session) 

def topic_comments(request,topic_id):                        #kim
    topic_comments_json = api_list.get_feature_topic_comments(request,topic_id)
    if not topic_comments_json or topic_comments_json['error'] != 0:
        return response_data_utils.error_comments(request,"评论不存在",__name__, topic_comments_json)
    topic_comments_json = process_comments(request,topic_comments_json)
    return topic_comments_json

def process_comments(request,comments):                      #kim
    for comment in comments["commentList"]:
        comment["creationTime"] = data_process_utils.get_time_since(comment['creationTime'])
        if comment["rComment"]:
            comment["rComment"]["content"] = string_utils.truncate(comment["rComment"]["content"])
    return comments

def topic_info_comments(request,topic_id,mark):
    if request.is_ajax:
        topic_info_comments_json = api_list.get_topic_info_comments(request,topic_id,mark,0,20)
        if topic_info_comments_json.get("commentList"):
            process_comments(request,topic_info_comments_json)
            next_page_url = reverse("topic:topic_info_comments",kwargs={"topic_id":topic_id,"mark":topic_info_comments_json["mark"]})
            meta = {"commentsTopic":topic_info_comments_json}
            t  = loader.get_template("topic/topic_comments.html")
            c  = RequestContext(request,meta)
            meta_dic = {'html':t.render(c),'url':next_page_url}
            return HttpResponse(json.dumps(meta_dic),content_type="application/json")
 
def topic_list(request, mark=0):
    is_ajax = request.is_ajax()
    try:
        topic_result = api_list.get_feature_topic_list(request, mark)
        if topic_result['error'] == 0 :
            process_topic_data(topic_result)
            next_request_url = ""
            if str(topic_result['mark']) != "0":
                next_request_url = reverse('topic:topic_list', kwargs ={"mark":topic_result['mark']})
            meta_data = {'featureTopicList' : topic_result["featureTopicList"], 'url':next_request_url ,'nav':'topic'}
            if is_ajax:
                context = RequestContext(request, meta_data)
                template = loader.get_template('topic/topic_list.html')
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                meta_data = response_data_utils.pack_data(request, meta_data)
                return render(request, 'topic/topic_index.html', meta_data)
    except Exception,e:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)

def new_topic_list(request,mark=0,order=0):                  #kim
    is_ajax = request.is_ajax()
    new_topic_result = api_list.get_feature_topic_list(request,mark,order)
    if new_topic_result and new_topic_result['error']!=0: 
        response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__,new_topic_result) 
    try:
        if is_ajax:
            process_topic_data(new_topic_result)
            next_request_url = ""
            if str(new_topic_result['mark']) != "0":
                next_request_url = reverse('topic:new_topic_list',kwargs={"mark":new_topic_result['mark']})
            meta_data = {'newTopicList':new_topic_result['featureTopicList'],'url':next_request_url }
            context = RequestContext(request, meta_data)
            template = loader.get_template('topic/topic_new.html')
            response_json = {'html':template.render(context), 'url':next_request_url}
            return HttpResponse(json.dumps(response_json), content_type="application/json")
    except Exception,e:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__,e) 

       
def process_topic_url(uid, topic_data):
    if topic_data.get('featureTopic'):
        content_list = topic_data['featureTopic'].get('contentList')
    if content_list == None:
      return None
    for content_info in content_list:
      link = content_info.get("link")
      if link and link['data'] and link['data'].startswith("http:"):
        if uid != None and uid != "":
          link['data'] = link['data'] + "?dp=" + str(uid)

def process_topic_data(topic_data):
  if topic_data.get('featureTopic'):
    pics = topic_data['featureTopic'].get('pics')
    topic_data['featureTopic']['digitalTime'] = topic_data['featureTopic']['creationTime']
    topic_data['featureTopic']['creationTime'] = time.strftime('%d %b',time.localtime(topic_data['featureTopic']['creationTime']/1000))
    topic_data['featureTopic']['digitalTime'] = time.strftime("%Y-%m-%d",time.localtime(topic_data['featureTopic']['digitalTime']/1000))
    if pics and len(pics) > 0 :
      topic_data['featureTopic']['org'] = pics[0]['org']
      topic_data['featureTopic']['width'] = pics[0]['width']
      topic_data['featureTopic']['height'] = pics[0]['height']
    content_list = topic_data['featureTopic'].get('contentList')
    if content_list:
      for content_info in content_list:
        content_sub_list = content_info.get("content")
        if content_sub_list:
           for sub_content_info in content_sub_list:
             temp_text = sub_content_info.get("text")
             if temp_text:
               sub_content_info["text"] = string_utils.replace_text_newline(cgi.escape(temp_text))
    if topic_data['featureTopic'].get("introduction"):
        if not topic_data['featureTopic']['introduction'].strip():
            topic_data['featureTopic']['introduction'] = topic_data['featureTopic']['introduction'].strip()
    if topic_data['featureTopic'].get("conclusion"):
        if not topic_data['featureTopic']['conclusion'].strip():
            topic_data['featureTopic']['conclusion'] = topic_data['featureTopic']['conclusion'].strip()


  if topic_data.get('featureTopicList'):
    for topic in topic_data['featureTopicList']:
      pics = topic.get('pics')
      topic['creationTime']  = time.strftime('%d %b',time.localtime(topic['creationTime']/1000))
      if pics and len(pics) > 0 :
        topic['org'] = pics[0]['org']
        topic['width'] = pics[0]['width']
        topic['height'] = pics[0]['height']
