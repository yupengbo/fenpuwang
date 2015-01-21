# -*- coding: utf-8 -*-

from django.conf import settings
import requests
from apps.utils import response_data_utils
import json
"""
Get base url for api request.
"""
def get_base_url():
    if settings.DEBUG:
        #base_url = "http://testapi.dabanniu.com/v2/"
        base_url = "http://api.dabanniu.com/v2/"
    else:
        base_url = "http://api.dabanniu.com/v2/"
    return base_url

def build_error_response(errorString):
    return {'error':1,'errorString':errorString}

def get_result(req, api_url, params):
    build_params(req,params)
    response = request('POST', api_url, params);
    result = build_error_response("server is busy-30331")
    try:
        if response.status_code == requests.codes.ok:
            result = response.json()
    except Exception,e:
        result = build_error_response("server is busy-30332")
    return result

def request(method, api_name, params, time_out=30.0):
    api_str = get_base_url() + api_name
    print api_str
    print params
    return requests.request(method, api_str, data = params, timeout = time_out)

def build_params(request,params):
    if not params:
       params = {}
    if not request:
      return params
    device = response_data_utils.get_user_device(request)
    device = 'm_' + device
    params['channel'] = 'm_website'
    params['device'] = device
    params['appName'] = 'm_fenpu'
    return params

def get_question_detail(req, question_id, has_question_details, has_related_question, mark):
    params = {'questionId': question_id, 'hasBody': has_question_details,
              'hasOtherQuestion':has_related_question, 'mark':mark, 'isRed':1}
    return get_result(req , 'getQuestionDetail.do', params)

#def get_product_detail(req, product_id, has_product_details = 0, pre = 20, mark = 0):
#    params = {'productId': product_id, 'hasBody': has_product_details, 'pre': pre, 'mark': mark}
#    return get_result(req, 'getProductInfo.do', params)

def get_product_info_by_id(req, product_id ):
    params = {'productId': product_id }
    build_params(req,params)
    return get_result(req, 'getProductInfoById.do', params)

def get_related_question_by_product_id(req, product_id, mark = 0):
    params = {'productId': product_id, 'mark': mark}
    return get_result(req, 'getRelatedContentByProduct.do', params)

def get_product_by_category(req, query_type, order, category_id, filter_category_id, pre, mark):
    params = {'type': query_type, 'order': order, 'pre': pre, 'mark': mark,
              'categoryId': category_id, 'filterCategoryId': filter_category_id}
    return get_result(req, 'listProductsByCategory.do', params)

def get_product_feeds(req, category_id = 0, pre = 20, mark = 0):
    params = {'pre': pre, 'mark': mark, 'categoryId': category_id, 'onlyFeatureQuestion': 1}
    return get_result(req, 'listProductFeeds.do', params)

def search(req, keyword, search_type = 0, pre = 20, mark = 0,isRed = 1,order = 0):
    params = {'pre': pre, 'mark': mark, 'type': search_type, 'keyword': keyword,'isRed':isRed,'order':order}
    return get_result(req, 'searchAll.do', params)

def get_feature_topic_list(req, mark = 0):
    params = {'mark': mark}
    return get_result(req, 'listFeatureTopic.do', params)

def get_feature_topic_info(req, feature_topic_id, topicVersion = 1):
    params = {'featureTopicId': feature_topic_id, 'topicVersion': topicVersion}
    return get_result(req, 'getFeatureTopicInfo.do', params)

def get_user_change_log(req, sessionKey, mark = 0):
    params = {'sessionKey': sessionKey,  'mark': mark}
    return get_result(req, 'listUserChangeLog.do', params)

def get_user_change_info(req, sessionKey):
    params = {'sessionKey': sessionKey}
    return get_result(req, 'getUserChangeInfo.do', params)
