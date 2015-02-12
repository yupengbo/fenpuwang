from django.conf.urls import patterns, url
from apps.cart import views

urlpatterns = patterns('',
#  url(r'^$', views.cart_list , name='cart_list'),
  url(r'^$', views.cart_index , name='cart_index'),
  url(r'^setcontact$', views.set_contact , name='set_contact'),
  url(r'^order_pay$', views.order_pay , name='order_pay'),
)

