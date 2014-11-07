from django.conf.urls import patterns, url

from apps.products import views

urlpatterns = patterns('',
    url(r'^/$', views.product_detail, name='product_detail'),
)

