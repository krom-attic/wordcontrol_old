from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView, TemplateView

from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from django_filters.views import FilterView

from wordengine import filters
from wordengine import forms
from wordengine.lexeme_utils.updater import update_lexeme_entry
from wordengine import models


def index(requst):
    return redirect('wordengine:list_lexeme_entry')


class InlineFormsetCreateView(CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = kwargs.get('formsets')
        if formsets:
            context.update(formsets)
        else:
            context.update({formset: formset_class() for formset, formset_class in self.inlines.items()})
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        errors = False
        if form.is_valid():
            self.object = form.save(commit=False)
        else:
            errors = True
        inlines = {}
        for formset in self.inlines:
            inlines[formset] = self.inlines[formset](self.request.POST, instance=self.object)
            if not inlines[formset].is_valid():
                errors = True
        if errors:
            return self.forms_invalid(form, inlines)
        else:
            return self.forms_valid(form, inlines)

    def form_invalid(self, form):
        pass

    def forms_invalid(self, form, inlines):
        self.form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form, formsets=inlines))

    def form_valid(self, form):
        self.object.save()

    def forms_valid(self, form, inlines):
        self.form_valid(form)
        for formset in inlines.values():
            formset.save()
        return HttpResponseRedirect(self.get_success_url())


class SaveUserMixIn:

    def form_valid(self, form):
        setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)


class DictCreateView(LoginRequiredMixin, SaveUserMixIn, InlineFormsetCreateView):

    model = models.Dictionary
    fields = ['caption']
    inlines = {'ws_in_dict_formset': forms.WSInDictFormset}
    user_field = 'maintainer'


class DictListView(LoginRequiredMixin, ListView):

    model = models.Dictionary

    def get_queryset(self):
        return super().get_queryset().filter(maintainer=self.request.user)


class DictDetailView(DetailView):

    model = models.Dictionary


class AddPermsDict(TemplateView):
    pass


class LexemeEntryFilterMixIn:

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


def save_lexeme_entry(form):
    changed_entry, wordforms, affected_entries = update_lexeme_entry(form.save(commit=False))
    # TODO Do all save in one transaction
    for lexeme_entry in [changed_entry] + affected_entries:
        lexeme_entry.save(explicit=True)
    for wordform in wordforms:
        # TODO Why doesn't it happen automatically?
        wordform.lexeme_entry_id = wordform.lexeme_entry.id
        wordform.save()
    return changed_entry


class LexemeEntryCreateView(UserFormKwargsMixin, LoginRequiredMixin, CreateView):
    model = models.LexemeEntry
    form_class = forms.DictEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'dictionary': models.Dictionary.objects.get(id=13)})
        return context

    def form_valid(self, form):
        self.object = save_lexeme_entry(form)
        return HttpResponseRedirect(self.get_success_url())


class LexemeEntryDetailView(LexemeEntryFilterMixIn, DetailView):
    model = models.LexemeEntry

    # def get(self, request, *args, **kwargs):
    #     try:
    #         return super().get(request, *args, **kwargs)
    #     except MultipleObjectsReturned:
    #         return redirect('wordengine:disambig_lexeme_entry', *args, **kwargs)


class LexemeEntryUpdateView(LexemeEntryFilterMixIn, UpdateView):
    model = models.LexemeEntry
    fields = ['syntactic_category', 'forms_text', 'relations_text', 'translations_text', 'sources_text']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.dictionary.maintainer:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('wordengine:view_lexeme_entry', pk=self.object.pk)

    def form_valid(self, form):
        self.object = save_lexeme_entry(form)
        return HttpResponseRedirect(self.get_success_url())

# class LexemeEntryListView(LexemeEntryFilterMixIn, ListView):
#     model = models.LexemeEntry


class LexemeEntryFilterView(LexemeEntryFilterMixIn, FilterView):
    filterset_class = filters.LexemeEntryFilter
    paginate_by = 20


# LEGACY VIEWS BELOW. DO NOT USE!

from wordengine.views_legacy import *
