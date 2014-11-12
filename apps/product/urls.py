from django.conf.urls import patterns, url

from apps.product import views

urlpatterns = patterns('',
  url(r'^(?P<product_id>\d+)/$', views.product_detail, name='question_detail'),
  url(r'^(?P<product_id>\d+)/mark/(?P<mark>\d+)/$', views.question_list, name='question_list'),
)

