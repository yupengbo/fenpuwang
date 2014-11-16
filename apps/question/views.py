# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from apps.api import api_list
from apps.utils import data_process_utils
import requests
import json

def question_details(request, question_id):
    try:
        question_obj = api_list.get_question_detail(question_id, 1, 1, 0)
        if question_obj['error'] == 0:
            process_question_data(question_obj)
            next_page_url = ''  # for next page ajax loading
            if int(question_obj['mark']) > 0:
                next_page_url = reverse('question:answer_list',
                                        kwargs = {'question_id' : question_id, 'mark' : question_obj['mark']})
            return render(request, 'question/question.html',
                          {'question':question_obj, 'question_id':question_id, 'url' : next_page_url})
    except Exception as e:
        print e
        raise Http404
    raise Http404

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
            answers_obj = api_list.get_question_detail(question_id, 0, 0, mark)
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
        except Exception as e:
            raise Http404
    else:
        raise Http404

def process_question_data(question_obj):
    """
    process question dictionary returned from api.
    :param question_obj:
    :return:
    """

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
    for answer in answers:
        answer['user']['profile'] = data_process_utils.get_user_profile_str(answer['user'])
        if answer['isBest'] > 0:
            answer['content'] = u"最佳回答：" +  answer['content']
