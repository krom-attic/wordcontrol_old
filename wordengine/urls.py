from django.conf.urls import patterns, url
from wordengine import views

urlpatterns = patterns('',
                       url(r'^add/word$', views.AddWordFormView.as_view(), name='add_wordform'),
                       url(r'^$', views.index, name='index'),
                       url(r'^dosmth$', views.DoSmthWordFormView.as_view(), name='do_something'),
                       url(r'^result$', views.action_result_view, name='action_result'),
                       url(r'^view/lexeme/(?P<lexeme_id>\d+)$', views.ShowLexemeDetailsView.as_view(),
                           name='show_lexemedetails'),
                       url(r'^view/words$', views.ShowWordFormListView.as_view(), name='show_wordlist'),
                       url(r'^delete/word/(?P<wordform_id>\d+)$', views.delete_wordform, name='delete_wordform')
)