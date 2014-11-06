from django.shortcuts import render
from django.http import HttpResponse
import requests

from apps.api import api_list




# Create your views here.
def question_details(request, product_id):
    r = api_list.get_question_detail(product_id, 1)
    if r.status_code == requests.codes.ok:
        question_obj = r.json()
        return render(request, 'product/product.html', {'question':question_obj})
    else:
        return HttpResponse("product id invalid")

