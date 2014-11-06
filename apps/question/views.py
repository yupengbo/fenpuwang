from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list



# Create your views here.
def question_details(request, question_id):
    try:
        question_obj = api_list.get_question_detail(question_id, 1)
        if question_obj['error'] == 0:
            return render(request, 'question/question.html', {'question':question_obj})
    except Exception,e:
        raise Http404
    raise Http404
