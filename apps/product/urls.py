from django.conf.urls import patterns, url

from apps.product import views

urlpatterns = patterns('',
    url(r'^(?P<product_id>\d+)/$', views.product_detail, name='product_detail'),
)

