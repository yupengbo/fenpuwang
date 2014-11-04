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


def request(method, api_name, params, time_out=30.0):
    api_str = get_base_url() + api_name
    return requests.request(method, api_str, params = params, timeout = time_out)

def get_question_detail(question_id, has_question_details):
    params = {'questionId': question_id, 'hasBody': has_question_details}
    return request('POST', 'getQuestionDetail.do', params)

