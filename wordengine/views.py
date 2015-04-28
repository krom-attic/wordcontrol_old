from wordengine import models

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.views.generic import UpdateView, CreateView, DetailView, ListView


def index(requst):
    return redirect('wordengine:list_lexeme_entry')


class LexemeEntryFilterMixIn():

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'lang_code' in self.kwargs:
            try:
                language = models.Language.objects.get(iso_code=self.kwargs['lang_code'].lower())
            except ObjectDoesNotExist:
                language = models.Language.objects.get(pk=self.kwargs['lang_code'])
            queryset = queryset.filter(language=language)
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            queryset = queryset.filter(slug=slug)
        if 'disambig' in self.kwargs:
            queryset = queryset.filter(disambig=self.kwargs['disambig'])

        return queryset


class LexemeEntryCreateView(CreateView):
    model = models.LexemeEntry
    fields = ['dictionary', 'language', 'syntactic_category', 'forms_text', 'relations_text', 'translations_text',
              'sources_text']


class LexemeEntryDetailView(LexemeEntryFilterMixIn, DetailView):
    model = models.LexemeEntry

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except MultipleObjectsReturned:
            return redirect('wordengine:disambig_lexeme_entry', *args, **kwargs)


class LexemeEntryUpdateView(LexemeEntryFilterMixIn, UpdateView):
    model = models.LexemeEntry
    fields = ['syntactic_category', 'forms_text', 'relations_text', 'translations_text', 'sources_text']


class LexemeEntryListView(LexemeEntryFilterMixIn, ListView):
    model = models.LexemeEntry

# LEGACY VIEWS BELOW. DO NOT USE!

from wordengine.views_legacy import *