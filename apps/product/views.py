from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list

#def convert_num(num):
#  if num == None or num == "":
#    return "0"
#  return num
 
# Create your views here.
def product_detail(request, product_id):
  has_product_info =  1
  product_json = api_list.get_product_detail(product_id, has_product_info)
  try:
    if product_json == None or product_json == "":
      return HttpResponse("product id invalid")
    print product_json 
    return render(request, 'product/product.html', {'product':product_json})
  except Exception,e:
    raise Http404
