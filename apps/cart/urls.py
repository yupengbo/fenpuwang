from django.conf.urls import patterns, url
from apps.cart import views

urlpatterns = patterns('',
  url(r'^$', views.cart_list , name='cart_list'),
)

