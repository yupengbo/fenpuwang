from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
from apps.api import api_list
from apps.utils import data_process_utils
from apps.utils import string_utils

# Create your views here.
def index(request):
    try:
        feed_result = api_list.get_product_feeds()
        if feed_result['error'] == 0 :
            process_feed_data(feed_result)
            return render(request, 'feed/feeds.html', {'feeds' : feed_result})
    except Exception,e:
        print e
        raise Http404
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
