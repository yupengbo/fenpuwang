# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.game import views

urlpatterns = patterns('',
  url(r'^makeup/(?P<activity_key>\w+)/$', views.makeup, name='makeup'),
  url(r'^makeup/get$', views.get, name='makeup_get'),
)

