from django.conf.urls import patterns, url

from apps.question import views

urlpatterns = patterns('',
    url(r'^(?P<question_id>\d+)/$', views.question_details, name='question_details'),
    url(r'^(?P<question_id>\d+)/mark/(?P<mark>\d+)/$', views.answer_list, name='answer_list'),
)

