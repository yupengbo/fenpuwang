# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.ucenter import views

urlpatterns = patterns('',
  url(r'^signup/$', views.signup, name='signup'),
  url(r'^sendCode/$', views.sendCode, name='sendCode'),
)
