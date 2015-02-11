from django.conf.urls import patterns, url

from apps.order import views

urlpatterns = patterns('',
  url(r'^$', views.order_detail, name='order_detail'),
  url(r'/pay$', views.order_pay, name='order_pay'),
)

