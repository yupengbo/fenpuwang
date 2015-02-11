#coding:UTF-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import json
import requests
from apps.api import api_list
from apps.utils import string_utils, response_data_utils
import cgi



