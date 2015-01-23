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

def download(request):
    return render(request, 'download.html')
