from django.conf.urls import patterns, url

from apps.question import views

urlpatterns = patterns('',
    url(r'^(?P<product_id>\d+)/$', views.product_details, name='product_details'),
)

