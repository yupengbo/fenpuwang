# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list, static_data
from apps.utils import data_process_utils, response_data_utils, string_utils
import json
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    try:
        feed_obj = api_list.get_product_feeds(request)
        nav_list = static_data.get_nav_data() 
        if feed_obj['error'] == 0 :
            process_feed_data(feed_obj)
            next_request_url = reverse('feed:feed_list', kwargs ={"categoryid" : 0, "mark": feed_obj['mark']}) 
            meta = response_data_utils.pack_data(request, {'feeds' : feed_obj['feedList'],'nav_list' : nav_list , 'url' : next_request_url, "nav": "index"})
            return render(request, 'feed/feeds.html', meta)
        else:
            return response_data_utils.error_response(request, None, __name__, feed_obj)
    except Exception,e:
        return response_data_utils.error_response(request, None, __name__, e)
def feed_list(request, categoryid, mark):
    if request.is_ajax(): #仅接受ajax请求
        try:
            feed_obj = api_list.get_product_feeds(request, categoryid, 20, mark)
            if feed_obj['error'] == 0:
                process_feed_data(feed_obj)
                template = loader.get_template('feed/feedList.html')
                context = RequestContext(request, {'feeds': feed_obj['feedList']})
                next_request_url = ""
                if str(feed_obj['mark']) != "0":
                    next_request_url = reverse('feed:feed_list', kwargs ={"categoryid" : categoryid, "mark" : feed_obj['mark']})
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                return response_data_utils.error_response(request, None, __name__, feed_obj)
        except Exception as e:
            return response_data_utils.error_response(request, None, __name__, e)
	return response_data_utils.error_response(request, None,  __name__, " not ajax")

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
        else:
            feed['question'] = {"questionId":0}
