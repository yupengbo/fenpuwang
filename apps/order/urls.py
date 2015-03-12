from django.conf.urls import patterns, url

from apps.order import views

urlpatterns = patterns('',
  url(r'^$', views.order_list, name='order_list'),
  url(r'^list/(?P<mark>\d+)/$', views.ajax_order_list, name='ajax_order_list'),
  url(r'^detail/(?P<order_id>\d+)/$', views.order_detail, name="order_detail"),
  url(r'^submit/$', views.submit_order, name='submit_order'),
  url(r'^bankpay/$', views.pay_order, name='pay_order'),
  url(r'^ajax_submit/$', views.ajax_submit_order, name='ajax_submit_order'),
  url(r'^topay/$', views.to_pay_order, name='to_pay_order'),
  url(r'^alipay/$', views.alipay_order, name='alipay_order'),
  url(r'^wxpay/$', views.wxpay_order, name='wxpay_order'),
#  url(r'^cart_num/$',views.cart_num,name="cart_num"),
)

