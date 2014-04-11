from django.conf.urls import patterns, url
from wordengine import views

urlpatterns = patterns('',
                       url(r'^add/word$', views.AddWordformView.as_view(), name='add_wordform_lexeme'),  # Depricated?
                       url(r'^add/word/use=(?P<language>\d*)&(?P<syntactic_category>\d*)&(?P<spelling>\w*)$',
                           views.AddWordformView.as_view(), name='add_wordform_lexeme'),
                       url(r'^add/word/like=(?P<first_lexeme>\d*)$', views.AddWordformView.as_view(),
                           name='add_wordform_lexeme'),
                       url(r'^add/word/addto=(?P<lexeme_id>\d+)$', views.AddWordformView.as_view(), name='add_wordform'),
                       url(r'^$', views.index, name='index'),
                       url(r'^dosmth$', views.DoSmthWordformView.as_view(), name='do_something'),
                       url(r'^view/lexeme/(?P<lexeme_id>\d+)$', views.ShowLexemeDetailsView.as_view(),
                           name='show_lexemedetails'),
                       url(r'^view/words$', views.ShowLexemeListView.as_view(), name='show_wordlist'),
                       url(r'^delete/word/(?P<wordform_id>\d+)$', views.delete_wordform, name='delete_wordform'),
                       url(r'^add/translation/addto=(?P<lexeme_id>\d+)$', views.AddTranslationView.as_view(),
                           name='add_translation')
                       )
