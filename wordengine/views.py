from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView

from braces.views import LoginRequiredMixin
from django_filters.views import FilterView

from wordengine import models
from wordengine import filters
from wordengine import forms


def index(requst):
    return redirect('wordengine:list_lexeme_entry')


class InlineFormsetCreateView(CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = kwargs.get('formsets')
        if formsets:
            context.update(formsets)
        else:
            for formset_class in self.inlines:
                context[formset_class] = self.inlines[formset_class]()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        errors = False
        if form.is_valid():
            self.object = form.save(commit=False)
        else:
            errors = True
        form.inlines = {}
        for formset_class in self.inlines:
            form.inlines[formset_class] = self.inlines[formset_class](self.request.POST, instance=self.object)
            if not form.inlines[formset_class].is_valid():
                errors = True
        if errors:
            return self.form_invalid(form)
        else:
            return self.form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formsets=form.inlines))

    def form_valid(self, form):
        self.object.save()
        for formset in form.inlines.values():
            formset.save()
        return HttpResponseRedirect(self.get_success_url())


class SaveUserMixIn():

    def form_valid(self, form):
        setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)


class DictCreateView(LoginRequiredMixin, SaveUserMixIn, InlineFormsetCreateView):

    model = models.Dictionary
    fields = ['caption']
    inlines = {'ws_in_dict_formset': forms.WSInDictFormset}
    user_field = 'maintainer'


class DictListView(ListView):
    model = models.Dictionary


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


class LexemeEntryFilterView(LexemeEntryFilterMixIn, FilterView):
    filterset_class = filters.LexemeEntryFilter


# LEGACY VIEWS BELOW. DO NOT USE!

from wordengine.views_legacy import *