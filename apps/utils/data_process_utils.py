# -*- coding: utf-8 -*-
"""
This module process data from API requests. For example, timestamp process, skin type process, etc.
:author Hui
"""

import time

def get_time_since(since):
    """
    get time description since timestamp.
    :param since:
    :return: string convert time to description, eg 2天前
    """
    now =  int(time.time())
    time_diff = (now - int(since) / 1000);
    day = time_diff / (3600*24);
    month = day / 30;
    year = month / 12;
    if year > 0:
        return str(year) + "年前"
    if month > 0:
        return str(month) + "月前"
    if day > 0:
        return str(day) + "天前"

    hour = time_diff / 3600;
    if hour > 0:
        return str(hour) + "小时前"
    mins = time_diff / 60;
    if mins > 0:
        return str(mins) + "分钟前"

    return "刚刚"

def get_user_profile_str(user):
    """
    get formatted user profile string from user dictionary, eg 混合肌，32岁
    :param user: a dictionary of user information, we use 'skinType' and 'ages' keys here.
    :return:
    """
    skin_desc = ""
    if 'skinType' in user:
        skin_type = user['skinType']
        if skin_type == 1:
            skin_desc = u"混合皮"
        elif skin_type == 2:
            skin_desc = u"油皮"
        elif skin_type == 3:
            skin_desc = u"干皮"

    age_desc = ""
    if 'ages' in user:
        age_desc = user['ages']

    if skin_desc and age_desc:
        return skin_desc + u"，" + age_desc
    elif skin_desc:
        return skin_desc
    elif age_desc:
        return age_desc
    else:
        return ""