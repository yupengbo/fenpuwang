from django.conf.urls import patterns, include, url
from apps.activity import views

urlpatterns = patterns('',
  url('^$',views.active,name = 'active'),
) 
