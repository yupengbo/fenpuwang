# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list
from apps.utils import data_process_utils
import pdb

def question_details(request, question_id):
    try:
        question_obj = api_list.get_question_detail(question_id, 1, 1)
        if question_obj['error'] == 0:
            process_question_data(question_obj)
            return render(request, 'question/question.html', {'question':question_obj})
    except Exception as e:
        return HttpResponse(e)
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

    for answer in question_obj['answerList']:
        answer['user']['profile'] = data_process_utils.get_user_profile_str(answer['user'])
        if answer['isBest'] > 0:
            answer['content'] = u"最佳回答：" +  answer['content']

    # 由于相关问题要插到回答中，如果回答数大于3，将回答分成两部分，方便template展示
    answer_num = len(question_obj['answerList'])
    if answer_num > 3:
        question_obj['answerPart1'] = question_obj['answerList'][0 : 3]
        question_obj['answerPart2'] = question_obj['answerList'][3 : answer_num]
    elif answer_num > 0:
        question_obj['answerPart1'] = question_obj['answerList'][0 : answer_num]





