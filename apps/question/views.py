# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from apps.api import api_list
from apps.utils import data_process_utils,string_utils, response_data_utils, weixin_auth_utils
import requests
import json
import cgi
import logging

logger = logging.getLogger('django')
def question_list(request,mark=0):                                     
    is_ajax = request.is_ajax()
    question_list_json = api_list.get_product_feeds(request,0,20,mark)
    try:
        if question_list_json and question_list_json['error']==0:
            process_question_time(question_list_json)
            next_page_url = ""
            if question_list_json['mark']!=0:
                next_page_url = reverse("question:question_list_choice",kwargs={'mark':question_list_json['mark']})
            meta_data = {'questionList':question_list_json['feedList'],'url':next_page_url, 'nav':'question'}
            if is_ajax:
                template = loader.get_template("question/questionList.html")
                context = RequestContext(request,meta_data)
                response_json = {'html':template.render(context),'url':next_page_url}
                response_json = json.dumps(response_json)
                return HttpResponse(response_json,content_type="application/json")
            else:
                meta_data = response_data_utils.pack_data(request,meta_data)
                return render(request,'question/questionIndex.html',meta_data) 
    except Exception,e:
        return response_data_utils.error_response(request,None, __name__, e)

def new_question_list(request,mark):                     
    question_new_json = api_list.get_question_new(request,mark)
    try:
        if question_new_json and question_new_json['error']==0:
            process_question_time(question_new_json)
            next_page_url=""
            if question_new_json['mark']!=0:
                next_page_url = reverse("question:question_list_new",kwargs={'mark':question_new_json['mark']})
            meta_data = {'questionNew':question_new_json['questionList'],'url':next_page_url}
            template = loader.get_template("question/questionNew.html")
            context = RequestContext(request,meta_data)
            response_json = {'html':template.render(context),'url':next_page_url}
            response_json = json.dumps(response_json)
            return HttpResponse(response_json,content_type="application/json")
    except Exception,e:
        return response_data_utils.error_response(request,None, __name__, e)

def process_question_time(data):
    if data.get('feedList'):
        for question in data['feedList']:
            if question['question'].get('creationTime'):
                question['question']['creationTime'] = data_process_utils.get_time_since(question['question']['creationTime']) 
    if data.get('questionList'):
        for new_question in data['questionList']:
            if new_question.get('creationTime'):
                new_question['creationTime'] = data_process_utils.get_time_since(new_question['creationTime'])
  
def question_details(request, question_id):
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

    if dp != "" and dp != None:
      api_list.bind_user(request, session, dp)
    else:
      dp = None
    # end 
    try:
        question_obj = api_list.get_question_detail(request, question_id, 1, 1, 0)
        if question_obj['error'] == 0:
            process_question_data(question_obj)
            next_page_url = ''  # for next page ajax loading
            if int(question_obj['mark']) > 0:
                next_page_url = reverse('question:answer_list', kwargs = {'question_id' : question_id, 'mark' : question_obj['mark']})
            meta_data = response_data_utils.pack_data(request, {'navTitle':'问答详情', 'question':question_obj, 'question_id':question_id, 'url' : next_page_url})
            return weixin_auth_utils.fp_render(request, 'question/question.html', meta_data, session)
        else:
            return response_data_utils.error_response(request, "找不到这个问题！",  __name__, question_obj, session)
    except Exception as e:
        return response_data_utils.error_response(request,"找不到这个问题！", __name__, e, session)
@csrf_exempt
def answer_list(request, question_id, mark):
    """
    根据mark返回答案列表，仅接受ajax请求
    :param request:
    :param question_id:
    :param mark:
    :return:
    """
    if request.is_ajax():
        try:
            answers_obj = api_list.get_question_detail(request, question_id, 0, 0, mark)
            if answers_obj['error'] == 0:
                process_answers(answers_obj['answerList']);
                template = loader.get_template('question/answerList.html')
                context = RequestContext(request, {'answers': answers_obj['answerList']})
                next_page_url = ''  # for next page ajax loading
                if int(answers_obj['mark']) > 0:
                    next_page_url = reverse('question:answer_list',
                                            kwargs = {'question_id' : question_id, 'mark' : answers_obj['mark']})
                response_json = {'html':template.render(context), 'mark':answers_obj['mark'], 'url':next_page_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, answers_obj)
        except Exception as e:
            return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)
    return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, "not ajax")

def process_question_data(question_obj):
    """
    process question dictionary returned from api.
    :param question_obj:
    :return:
    """
    content = question_obj['question'].get("content")
    question_obj['question']['normal_title'] = string_utils.clear_link(question_obj['question']['title'])
    question_obj['question']['title'] = cgi.escape(question_obj['question']['title'])
    question_obj['question']['title'] = string_utils.replace_link(question_obj['question']['title'])
    if content:
        question_obj['question']['content'] = string_utils.replace_text_newline(cgi.escape(content))
        question_obj['question']['content'] = string_utils.replace_link(question_obj['question']['content'])
    else:
        question_obj['question']['content'] = ''
    # 转换时间显示格式
    question_obj['question']['creationTime'] = data_process_utils.get_time_since(question_obj['question']['creationTime'])

    # 将 skinType 和 ages 转换为页面显示的格式
    question_obj['question']['user']['profile'] = data_process_utils.get_user_profile_str(question_obj['question']['user'])

    process_answers(question_obj['answerList']);

    # 由于相关问题要插到回答中，如果回答数大于3，将回答分成两部分，方便template展示
    answer_num = len(question_obj['answerList'])
    if answer_num > 3:
        question_obj['answerPart1'] = question_obj['answerList'][0 : 3]
        question_obj['answerPart2'] = question_obj['answerList'][3 : answer_num]
    elif answer_num > 0:
        question_obj['answerPart1'] = question_obj['answerList'][0 : answer_num]

def process_answers(answers):
    """
    将answer中的用户profile转换成页面显示格式
    :param answers:
    :return:
    """
    has_best_answer = False
    for answer in answers:
        content = answer.get("content")
        if content:
            answer["content"] = string_utils.replace_text_newline(cgi.escape(content))
            answer["content"] = string_utils.replace_link(answer["content"])
        answer['user']['profile'] = data_process_utils.get_user_profile_str(answer['user'])

        if not has_best_answer and answer['isBest'] > 0:
            answer['content'] = u"最佳回答：" +  answer['content']
            has_best_answer = True
