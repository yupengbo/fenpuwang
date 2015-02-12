from django.conf.urls import patterns, url

from apps.order import views

urlpatterns = patterns('',
  url(r'^$', views.order_list, name='order_list'),
  url(r'^detail/(?P<order_id>\d+)/$', views.order_detail, name="order_detail"),
#  url(r'^cart_num/$',views.cart_num,name="cart_num"),
  
)

