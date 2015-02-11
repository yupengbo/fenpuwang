# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from apps.api import api_list
import requests
from apps.utils import string_utils, response_data_utils, data_process_utils
from apps.api import api_list, static_data
from django.core.urlresolvers import reverse
import json
import time
import cgi
import logging

logger = logging.getLogger('django')
def topic_list(request, mark=0):
    is_ajax = request.is_ajax()
    try:
        topic_result = api_list.get_feature_topic_list(request, mark)
        if topic_result['error'] == 0 :
            process_topic_data(topic_result)
            next_request_url = ""
            if str(topic_result['mark']) != "0":
                next_request_url = reverse('topic:topic_list', kwargs ={"mark":topic_result['mark']})
            meta_data = {'featureTopicList' : topic_result["featureTopicList"], 'url':next_request_url ,'nav':'topic'}
            if is_ajax:
                context = RequestContext(request, meta_data)
                template = loader.get_template('topic/topic_list.html')
                response_json = {'html':template.render(context), 'url':next_request_url}
                return HttpResponse(json.dumps(response_json), content_type="application/json")
            else:
                meta_data = response_data_utils.pack_data(request, meta_data)
                return render(request, 'topic/topic_index.html', meta_data)
    except Exception,e:
        return response_data_utils.error_response(request,"服务器忙，请稍后重试！", __name__, e)

