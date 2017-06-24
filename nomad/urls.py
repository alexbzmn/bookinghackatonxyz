from django.conf.urls import url

from . import views

app_name = 'nomad'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(create-question/$)', views.create_question_view, name='createq'),
    url(r'^(create-question/create$)', views.create_question_create, name='createqaction'),
    url(r'^(api/events$)', views.get_events, name='getevents')
]
