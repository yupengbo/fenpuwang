# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list, static_data
from apps.utils import data_process_utils
from apps.utils import string_utils
import json
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    try:
        feed_obj = api_list.get_product_feeds()
        nav_list = static_data.get_nav_data() 
        if feed_obj['error'] == 0 :
            process_feed_data(feed_obj)
            next_request_url = reverse('feed:feed_list', kwargs ={"categoryid" : 0, "mark" : feed_obj['mark']}) 
            return render(request, 'feed/feeds.html', {'feeds' : feed_obj['feedList'],'nav_list' : nav_list , 'url' : next_request_url})
    except Exception,e:
        print e
        raise Http404
    raise Http404

def feed_list(request, categoryid, mark):
    if request.is_ajax(): #仅接受ajax请求
        try:
            feed_obj = api_list.get_product_feeds( categoryid, 20, mark)
            if feed_obj['error'] == 0:
                process_feed_data(feed_obj)
                template = loader.get_template('feed/feedList.html')
                context = RequestContext(request, {'feeds': feed_obj['feedList']})
                next_request_url = reverse('feed:feed_list', kwargs ={"categoryid" : categoryid, "mark" : feed_obj['mark']})
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
        except Exception as e:
            return HttpResponse(e)
        raise Http404
    else:
        raise Http404

def process_feed_data(feed_obj):
    """
    process feed dictionary returned from api.
    :param feed_obj:
    :return:
    """

    for feed in feed_obj['feedList']:
        feed['user']['profile'] = data_process_utils.get_user_profile_str(feed['user'])
        if feed.get('answer'):
            feed['answer']['content'] = string_utils.truncate_text(feed['answer']['content'])
        if feed.get('question'):
            feed['question']['content'] = string_utils.truncate_text(feed['question']['content'])
