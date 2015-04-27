# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from apps.ucenter import views

urlpatterns = patterns('',
  url(r'^signup$', views.signup, name='signup'),
  url(r'^sendCode$', views.sendCode, name='sendCode'),
  url(r'^change$', views.change, name='change'),
  url(r'^change/(?P<sessionKey>\w+)/(?P<mark>\d+)/$', views.change, name='change_log_list'),
  url(r'^exchangeCode$',views.exchange,name='exchangeCode')
)

