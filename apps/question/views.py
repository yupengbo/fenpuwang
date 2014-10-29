from django.shortcuts import render
from django.http import HttpResponse
import requests

from apps.api import api_list




# Create your views here.
def question_details(request, question_id):
    r = api_list.get_question_detail(question_id, 1)
    if r.status_code == requests.codes.ok:
        question_obj = r.json()
        return render(request, 'question/question.html', {'question':question_obj})
    else:
        return HttpResponse("question id invalid")