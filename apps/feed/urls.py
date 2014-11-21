from django.conf.urls import patterns, url

from apps.feed import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^category/(?P<categoryid>\d+)/mark/(?P<mark>\d+)$', views.feed_list, name='feed_list'),
)

