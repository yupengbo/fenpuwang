# -*- coding: utf-8 -*-

import json
from django.conf import settings
"""
static data.
"""
def get_nav_data():
   #nav_list = ['2': u'面霜','4': u'乳液','6': u'面部精华','8': u'眼部护理','10': u'化妆水','12': u'洁面品','14': u'面膜','16': u'卸妆','18': u'bb/cc霜','20': u'粉底','22': u'粉饼','24': u'散粉','26': u'腮红','28': u'口红']
   #nav_list = {'2': u'面霜','4': u'乳液','6': u'面部精华','8': u'眼部护理','10': u'化妆水','12': u'洁面品','14': u'面膜','16': u'卸妆','18': u'bb/cc霜','20': u    '粉底','22': u'粉饼','24': u'散粉','26': u'腮红','28': u'口红'}
   nav_list = [('2', u'面霜'), ('4', u'乳液'), ('6', u'面部精华'), ('8', u'眼部护理'), ('10', u'化妆水'), ('12', u'洁面品'), ('14', u'面膜'), ('16', u'卸妆'), ('18', u'bb/cc霜'), ('20', u'粉底    '), ('22', u'粉饼'), ('24', u'散粉'), ('26', u'腮红'), ('28', u'口红')]
   return nav_list


products_index_data={}

def get_products_index_data():
   global products_index_data
   if not products_index_data:
      fp = open(settings.BASE_DIR + "/products.json", 'r')
      s = json.load(fp)
      fp.close()
      products_index_data = s
   return products_index_data
