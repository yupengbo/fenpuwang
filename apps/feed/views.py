from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list



# Create your views here.
def index(request):
    try:
        feed_result = api_list.get_product_feeds()
        if feed_result['error'] == 0 :
            return render(request, 'feed/feeds.html', {'feeds' : feed_result})
    except Exception,e:
        print e
        raise Http404
    raise Http404

