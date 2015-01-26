from django.conf.urls import patterns, url

from apps.question import views

urlpatterns = patterns('',
    url(r'^$',views.question_list,name='question_list'),
    url(r'^mark/(?P<mark>\d+)/choice/$',views.question_list,name='question_list_ajax'),
    url(r'^mark/(?P<mark>\d+)/new/$',views.new_question_list,name='question_list_new'),
    url(r'^(?P<question_id>\d+)/$', views.question_details, name='question_details'),
    url(r'^(?P<question_id>\d+)/mark/(?P<mark>\d+)/$', views.answer_list, name='answer_list'),
)

