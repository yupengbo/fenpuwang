from django.conf.urls import patterns, url
from apps.products import views

urlpatterns = patterns('',
  url(r'^$', views.products_recommend, name='products_recommend'),
  url(r'^recommend/(?P<mark>\d+)/$', views.products_recommend_list, name='products_recommend_list'),
  url(r'^category/$', views.products_index, name='products_index'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)$', views.productlist_by_category, name='query_by_category'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)$', views.productlist_by_category, name='query_by_category_order'),
#  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)/(?P<filter>\d+)$', views.productlist_by_category, name='query_by_category_order_filter'),
  url(r'^(?P<type>\d+)/(?P<category_id>\d+)/(?P<order>\d+)/(?P<filter>\d+)/(?P<mark>\d+)$', views.productlist_by_category, name='query_by_all'),
  url(r'^session/$', views.session, name='session'),
  url(r'^flashing/$', views.seckill, name='flashing'),
  url(r'^ajax_exists_qualification/$', views.ajax_exists_qualification, name='ajax_exists_qualification'),
  url(r'^ajax_get_stock/$', views.ajax_get_stock, name='ajax_get_stock'),
  url(r'^album/(?P<albumId>\d+)/$', views.album_detail, name='album_detail'),
  url(r'^product_info/(?P<productId>\d+)/$',views.product_info,name='product_info'),
)

