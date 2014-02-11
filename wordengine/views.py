from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib import messages
from wordengine import forms, models


# Common procedures here

def find_lexeme_wordforms(word_search):
    if word_search.is_valid():
        word_result = models.WordForm.objects.filter(spelling__istartswith=word_search.cleaned_data['search_for'])
        if word_search.cleaned_data['syntactic_category']:
            word_result = word_result.filter(lexeme__syntactic_category__exact=word_search.cleaned_data['syntactic_category'])
    #TODO Invalid search handling
    return word_result


# Actual views here

def index(request):
    return render(request, 'wordengine/index.html')


class DoSmthWordFormView(TemplateView):
    """Sandbox view"""

    some_object_class = forms.DoSmthWithIdForm
    template_name = 'wordengine/do_smth.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'smth_form': self.some_object_class()})

    def post(self, request, *args, **kwargs):
        if '_delete_wordform' in request.POST:
            word_form = get_object_or_404(models.WordForm, pk=request.POST['given_id'])
            # if the corresponding lexeme doesn't have another wordforms:
                # if it has a translation, block wordform deletion
                # if it doesn't, delete the lexeme and the wordform, record the deletion
            # if the lexeme has another wordforms, delete a wordform, record the deletion
            word_form.is_deleted = True
            word_form.save()
        elif '_restore_wordform' in request.POST:
            word_form = get_object_or_404(models.WordForm, pk=request.POST['given_id'])
            word_form.is_deleted = False
            word_form.save()
        return redirect(reverse('wordengine:action_result'))


class AddWordFormView(TemplateView):
    """New word addition view"""

    word_search_form_class = forms.SearchWordFormForm
    word_form_class = forms.WordFormForm
    lexeme_form_class = forms.LexemeForm
    source_form_class = forms.SourceSelectForm
    template_name = 'wordengine/add_word.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'word_search_form':self.word_search_form_class(),
                                                    'word_form': self.word_form_class(),
                                                    'lexeme_form': self.lexeme_form_class(),
                                                    'source_form': self.source_form_class()})

    def post(self, request, *args, **kwargs):
        is_saved = False
        lexeme_form = self.lexeme_form_class(request.POST)
        source_form = self.source_form_class(request.POST)
        if lexeme_form.is_valid() and source_form.is_valid():
            lexeme = lexeme_form.save()
            source = source_form.cleaned_data['source']
            change = models.DictChange(source=source, user_changer=request.user)
            change.save()
            word_form_initial = models.WordForm(lexeme=lexeme, dict_change_commit=change)
            word_form = self.word_form_class(request.POST, instance=word_form_initial)
            if word_form.is_valid():
                word_form.save()
                is_saved = True
        if (not is_saved) and (not '_just_search' in request.POST):
            return render(request, self.template_name, {'word_form': word_form, 'lexeme_form': lexeme_form,
                                                        'source_form': source_form})

        #TODO Make possible to select a lexeme from search results

        if '_continue_edit' in request.POST:
            return redirect(reverse('wordengine:index'))
        elif ('_add_new' in request.POST) or ('_just_search' in request.POST):
            return redirect(reverse('wordengine:add_wordform'))
        else:
            return redirect(reverse('wordengine:index'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordFormView, self).dispatch(*args, **kwargs)


class ShowWordFormListView(TemplateView):
    """Show a list of wordfomrs view"""

    word_search_class = forms.SearchWordFormForm
    template_name = 'wordengine/wordform_list.html'

    def get(self, request, *args, **kwargs):
        if request.GET:
            word_search = self.word_search_class(request.GET)
            word_result = find_lexeme_wordforms(word_search)
            return render(request, self.template_name, {'word_search': word_search,
                                                        'word_result': word_result, 'is_search': True})
        else:
            word_search = self.word_search_class()
            return render(request, self.template_name, {'word_search': word_search, 'is_search': False})


class ShowLexemeDetailsView(TemplateView):
    """Show details of lexeme view. Lexeme is indicated by spelling of a word"""

    template_name = 'wordengine/lexeme_details.html'

    def get(self, request, lexeme_id, *args, **kwargs):
        given_lexeme = get_object_or_404(models.Lexeme, pk=lexeme_id)
        lexeme_words = given_lexeme.wordform_set.all()
        return render(request, self.template_name, {'given_lexeme': given_lexeme, 'lexeme_words': lexeme_words})


@login_required
@transaction.atomic
def delete_wordform(request, wordform_id):
    given_wordform = get_object_or_404(models.WordForm, pk=wordform_id)
    #TODO handle 404 for wordform
    taken_lexeme = given_wordform.lexeme
    #TODO handle non-existant lexeme
    source = models.Source(pk=1)
    #TODO Is it ok to take the first source?

    if (taken_lexeme.wordform_set.count() == 1) and (taken_lexeme.translationbase_fst_set.count() +
                                                     taken_lexeme.translationbase_snd_set.count() > 0):
        messages.add_message(request, messages.ERROR, "The word has translations and thus can't be deleted")
    else:
        change = models.DictChange(source=source, user_changer=request.user)
        change.save()
        given_wordform.is_deleted = True
        deletion_record = models.WordFormDeleted(word_form=given_wordform, dict_change_delete=change)
        given_wordform.save()
        deletion_record.save()
        #TODO Check if deletion is correct?
        messages.add_message(request, messages.SUCCESS, "The word has been deleted")
    if taken_lexeme.wordform_set.filter(is_deleted__exact=False).count() == 0:
        return redirect(reverse('wordengine:show_wordlist'))
    else:
        return redirect(reverse('wordengine:show_lexemedetails', kwargs={'lexeme_id': taken_lexeme.id}))

