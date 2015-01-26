from django.conf.urls import patterns, url
from apps.topic import views

urlpatterns = patterns('',
  url(r'^$', views.topic_list , name='topic_index'),
  url(r'^mark/(?P<mark>\d+)$', views.topic_list, name='topic_list'),
  url(r'^mark/(?P<mark>\d+)/order/$',views.new_topic_list,name='new_topic_list'),
  url(r'^(?P<topic_id>\d+)/$', views.topic_info, name='topic_info'),
)

