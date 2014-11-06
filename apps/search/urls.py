from django.conf.urls import patterns, url

from apps.search import views

urlpatterns = patterns('',
    url(r'^(?P<keyword>\d+)/$', views.search, name='search'),
)

