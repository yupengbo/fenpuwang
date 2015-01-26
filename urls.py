from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^feed/', include('apps.feed.urls', namespace='feed')),
    url(r'^question/', include('apps.question.urls', namespace='question')),
    url(r'^product/', include('apps.product.urls', namespace='product')),
    url(r'^products/', include('apps.products.urls', namespace='products')),
    url(r'^search/', include('apps.search.urls', namespace='search')),
    url(r'^(topic/)?', include('apps.topic.urls', namespace='topic')),
	url(r'^ucenter/', include('apps.ucenter.urls', namespace='ucenter')),
    url(r'^download/$', views.download, name='download'),
)

