from django.conf.urls import patterns, url
from apps.cart import views

urlpatterns = patterns('',
  url(r'^$', views.cart_index , name='cart_index'),
  url(r'^setcontact$', views.set_contact , name='set_contact'),
)

