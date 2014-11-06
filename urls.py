from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('apps.feed.urls', namespace='feed')),
    url(r'^question/', include('apps.question.urls', namespace='question')),
    url(r'^product/', include('apps.product.urls', namespace='product')),
	url(r'^products/', include('apps.product.urls', namespace='product')),
	url(r'^search/', include('apps.search.urls', namespace='search')),
#	url(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

