from django.conf.urls import patterns, url

from wordengine import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^add/word$', views.AddWordformView.as_view(), name='add_wordform_lexeme'),  # Depricated?
                       url(r'^add/word/use=(?P<language>\d*)&(?P<syntactic_category>\d*)&(?P<spelling>\w*)$',
                           views.AddWordformView.as_view(), name='add_wordform_lexeme'),
                       url(r'^add/word/use=(?P<language>\d*)&(?P<syntactic_category>\d*)&(?P<first_lexeme_id>\d*)&(?P<spelling>\w*)$',
                           views.AddWordformView.as_view(), name='add_wordform_lexeme'),
                       url(r'^add/word/addto=(?P<lexeme_id>\d+)$', views.AddWordformView.as_view(), name='add_wordform'),
                       url(r'^dosmth$', views.DoSmthWordformView.as_view(), name='do_something'),
                       url(r'^view/words$', views.LexemeView.as_view(), name='show_wordlist'),
                       url(r'^view/words/(?P<lexeme_id>\d+)$', views.LexemeView.as_view(),
                           name='show_wordlist'),
                       url(r'^delete/word/(?P<wordform_id>\d+)$', views.delete_wordform, name='delete_wordform'),
                       url(r'^add/translation/addto=(?P<lexeme_id>\d+)$', views.AddTranslationView.as_view(),
                           name='add_translation'),
                       url(r'^add/translation/addto=(?P<lexeme_id>\d+)&(?P<second_lexeme_id>\d+)$',
                           views.AddTranslationView.as_view(), name='add_translation'),
                       url(r'^admin$', views.AdminView.as_view(), name='admin'),
                       url(r'^admin/language/(?P<language_id>\d+)$', views.LanguageSetupView.as_view(),
                           name='language_setup'),
                       url(r'^view/projects/(?P<project_id>\d+)$', views.ProjectSetupView.as_view(),
                           name='project_setup'),
                       url(r'^view/projects/?$', views.ProjectListView.as_view(), name='project_list'),
                       )