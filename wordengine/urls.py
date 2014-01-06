from django.conf.urls import patterns, url
from wordengine import views

urlpatterns = patterns('',
                       url(r'^add/word$', views.AddWordFormView.as_view(), name='add_wordform'),
                       url(r'^$', views.index, name='index')
)