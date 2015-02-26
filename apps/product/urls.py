from django.conf.urls import patterns, url

from apps.product import views

urlpatterns = patterns('',
  url(r'^(?P<product_id>\d+)/$', views.product_detail, name='product_detail'),
  url(r'^(?P<product_id>\d+)/official$', views.product_official, name='product_official'),
  url(r'^(?P<product_id>\d+)/mark/(?P<mark>\d+)/$', views.question_list, name='question_list'),
  url(r'^add_in_cart/$',views.add_in_cart,name="add_in_cart"),
  url(r'^del_in_cart/$',views.del_in_cart,name="del_in_cart"),
)

