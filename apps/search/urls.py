# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.search import views

urlpatterns = patterns('',
  url(r'^(?P<keyword>[^/]+)/$', views.search, name='search'),
  url(r'^(?P<keyword>[^/]+)/mark/(?P<mark>\d+)/$', views.question_list, name='question_list'),
)

