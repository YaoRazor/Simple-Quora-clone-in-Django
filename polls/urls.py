from django.conf.urls import patterns, url

from polls import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    #url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # # ex: /polls/5/results/
    #url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^ask/$', views.goto_add_page, name='ask'),
    url(r'^add_question/$', views.add_question, name='ask_question'),
    url(r'^(?P<question_id>\d+)/answer/$', views.goto_answer_page, name='answer'),
    url(r'^(?P<question_id>\d+)/add_answer/$', views.add_answer, name='answer_question'),
)