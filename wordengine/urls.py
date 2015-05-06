from django.conf.urls import patterns, url

from wordengine import views


urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='index'),
             url(r'^word/(?P<pk>\d+)/?$', views.LexemeEntryDetailView.as_view(), name='view_lexeme_entry'),
             url(r'^word/(?P<pk>\d+)/edit/?$', views.LexemeEntryUpdateView.as_view(), name='edit_lexeme_entry'),
             url(r'^word/(?P<lang_code>[\w-]+)/(?P<slug>[\w\- ]+)/?$', views.LexemeEntryDetailView.as_view(),
                 name='view_lexeme_entry'),
             url(r'^word/(?P<lang_code>[\w-]+)/(?P<slug>[\w\- ]+)/(?P<disambig>\d+)/?$',
                 views.LexemeEntryDetailView.as_view(),
                 name='view_lexeme_entry'),
             url(r'^word/(?P<lang_code>[\w-]+)/(?P<slug>[\w\- ]+)/edit/?$',
                 views.LexemeEntryUpdateView.as_view(), name='edit_lexeme_entry'),
             url(r'^words/?$', views.LexemeEntryFilterView.as_view(), name='list_lexeme_entry'),
             url(r'^word/(?P<lang_code>[\w-]+)/(?P<slug>[\w\- ]+)/\*/?$', views.LexemeEntryListView.as_view(),
                 name='disambig_lexeme_entry'),

            # LEGACY PATTERNS BELOW
             url(r'^add/word$', views.AddWordformView.as_view(), name='add_wordform_lexeme'),  # Depricated?
             url(r'^add/word/use=(?P<language>\d*)&(?P<syntactic_category>\d*)&(?P<spelling>\w*)$',
                 views.AddWordformView.as_view(), name='add_wordform_lexeme'),
             url(r'^add/word/use=(?P<language>\d*)&(?P<syntactic_category>\d*)&(?P<first_lexeme_id>\d*)&(?P<spelling>\w*)$',
                 views.AddWordformView.as_view(), name='add_wordform_lexeme'),
             url(r'^add/word/addto=(?P<lexeme_id>\d+)$', views.AddWordformView.as_view(), name='add_wordform'),
             url(r'^dosmth$', views.DoSmthWordformView.as_view(), name='do_something'),
             url(r'^view/words$', views.LexemeView.as_view(), name='view_words'),
             url(r'^view/words/(?P<lexeme_id>\d+)$', views.LexemeView.as_view(),
                 name='view_word'),
             url(r'^delete/word/(?P<wordform_id>\d+)$', views.delete_wordform, name='delete_wordform'),
             url(r'^add/translation/addto=(?P<lexeme_id>\d+)$', views.AddTranslationView.as_view(),
                 name='add_translation'),
             url(r'^add/translation/addto=(?P<lexeme_id>\d+)&(?P<second_lexeme_id>\d+)$',
                 views.AddTranslationView.as_view(), name='add_translation'),
             url(r'^admin$', views.AdminView.as_view(), name='admin'),
             url(r'^admin/language/(?P<language_id>\d+)$', views.LanguageSetupView.as_view(),
                 name='language_setup'),
             url(r'^view/projects/(?P<pk>\d+)$', views.ProjectSetupView.as_view(),
                 name='project_setup'),
             url(r'^view/projects/?$', views.ProjectListView.as_view(), name='view_projects'),
             # url(r'^update/project/(?P<pk>\d+)$', views.ProjectDictionaryUpdateView.as_view(),
             #     name='project_dict_update'),
             url(r'^add/?$', views.LexemeEntryCreateView.as_view(), name='add_lexeme_entry'),
             )