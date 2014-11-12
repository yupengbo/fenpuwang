from django.conf.urls import patterns, url

from apps.products import views

urlpatterns = patterns('',
  #url(r'^$', views.index, name='index'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)$', views.productlist_by_category, name='productlist_by_category'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)$', views.productlist_by_category, name='productlist_by_category'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)/(?P<filter>\d+)$', views.productlist_by_category, name='productlist_by_category'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)/(?P<filter>\d+)/(?P<mark>\d+)$', views.productlist_by_category, name='productlist_by_category'),
)

