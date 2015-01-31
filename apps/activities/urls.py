# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.activities import views

urlpatterns = patterns('',
  url(r'^(?P<activity_id>\d+)/$', views.activity, name='activity'),
  url(r'^openbonus/(?P<activity_id>\d+)/$', views.open_bonus, name='open_bonus'),
  url(r'^shareactivity/(?P<activity_id>\d+)/$', views.share_activity, name='share_activity'),
)

