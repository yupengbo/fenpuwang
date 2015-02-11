from django.conf.urls import patterns, url

from apps.orders import views
 
urlpatterns = patterns('',
  url(r'^$', views.orders_list, name='orders_list'),
 )

