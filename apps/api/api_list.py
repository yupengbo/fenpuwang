from django.conf import settings
import requests

"""
Get base url for api request.
"""
def get_base_url():
    if settings.DEBUG:
        base_url = "http://testapi.dabanniu.com/v2/"
    else:
        base_url = "http://api.dabanniu.com/v2/"
    return base_url

def build_error_response(errorString):
    return {'error':1,'errorString':errorString}

def get_result(response):
    result = build_error_response("server is busy-30331")
    try:
        if response.status_code == requests.codes.ok:
            result = response.json()
    except Exception,e:
        result = build_error_response("server is busy-30332")
    return result

def request(method, api_name, params, time_out=30.0):
    api_str = get_base_url() + api_name
    return requests.request(method, api_str, params = params, timeout = time_out)

def get_question_detail(question_id, has_question_details):
    params = {'questionId': question_id, 'hasBody': has_question_details}
    return get_result(request('POST', 'getQuestionDetail.do', params))

def get_product_detail(product_id, has_product_details, pre, mark):
    params = {'productId': product_id, 'hasBody': has_product_details, 'pre': pre, 'mark': mark}
    return request('POST', 'getProductInfo.do', params)

def get_product_by_category(query_type, order, category_id, filter_category_id, pre, mark):
    params = {'type': query_type, 'order': order, 'pre': pre, 'mark': mark, 'categoryId': category_id, 'filterCategoryId': filter_category_id}
    return request('POST', 'listProductsByCategory.do', params)
