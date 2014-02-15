from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from wordengine import forms, models


# Common procedures here

def find_lexeme_wordforms(word_search):
    if word_search.is_valid():
        word_result = models.WordForm.objects.filter(spelling__istartswith=word_search.cleaned_data['spelling'])
        if word_search.cleaned_data['language']:
            word_result = word_result.filter(lexeme__language__exact=word_search.cleaned_data['language'])
        elif word_search.cleaned_data['syntactic_category']:
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
        if '_restore_wordform' in request.POST:
            word_form = get_object_or_404(models.WordForm, pk=request.POST['given_id'])
            word_form.is_deleted = False
            word_form.save()
        return redirect('wordengine:action_result')


class AddWordFormViewBase(TemplateView):
    """New word addition base view"""

    lexeme_form_class = forms.LexemeForm
    word_form_class = forms.WordFormForm
    source_form_class = forms.SourceSelectForm
    template_name = 'wordengine/word_add.html'

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
        if not is_saved:
            return render(request, self.template_name, {'word_form': word_form, 'lexeme_form': lexeme_form,
                                                        'source_form': source_form})

        if '_continue_edit' in request.POST:
            return redirect('wordengine:index')
        elif ('_add_new' in request.POST) or ('_just_search' in request.POST):
            return redirect('wordengine:add_wordform')
        else:
            return redirect('wordengine:index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordFormViewBase, self).dispatch(*args, **kwargs)


class AddWordFormView(AddWordFormViewBase):
    """New word addition view (for existing lexeme)"""

    def get(self, request, *args, **kwargs):
        given_lexeme = models.Lexeme.objects.get(pk=kwargs.get('lexeme_id'))
        return render(request, self.template_name, {'given_lexeme': given_lexeme,
                                                    'word_form': self.word_form_class(),
                                                    'source_form': self.source_form_class()})


class AddWordLexemeFormView(AddWordFormViewBase):
    """New word addition view"""

    def get(self, request, *args, **kwargs):
        lexeme_form = self.lexeme_form_class(initial={'language': kwargs.get('language'),
                                                      'syntactic_category': kwargs.get('syntactic_category')})
        word_form = self.word_form_class(initial={'spelling': kwargs.get('spelling')})
        source_form = self.source_form_class()
        if kwargs.get('language'):
            lang_filter = Q(language=kwargs.get('language')) | Q(language=None)
            source_form.fields['source'].queryset = models.Source.objects.filter(lang_filter)
            word_form.fields['writing_system'].queryset = models.WritingSystem.objects.filter(lang_filter)
            word_form.fields['dialect_multi'].queryset = models.Dialect.objects.filter(lang_filter)
        if kwargs.get('syntactic_category'):
            synt_cat_filter = Q(syntactic_category=kwargs.get('syntactic_category')) | Q(syntactic_category=None)
            word_form.fields['gramm_category_set'].queryset = models.GrammCategorySet.objects.filter(synt_cat_filter)
        #TODO Correct this after gramm cat becomes language dependent
        #TODO Changing language or synt cat should trigger page reload (to update filtered fields)

        return render(request, self.template_name, {'word_form': word_form,
                                                    'lexeme_form': lexeme_form,
                                                    'source_form': source_form})


class ShowLexemeListView(TemplateView):
    """Show a list of wordfomrs view"""
    word_search_form_class = forms.SearchWordFormForm
    template_name = 'wordengine/lexeme_list.html'

    def get(self, request, *args, **kwargs):
        if not request.GET:
            return render(request, self.template_name, {'word_search': self.word_search_form_class(),
                                                        'is_search': False})
        else:
            word_search = self.word_search_form_class(request.GET)
            if '_just_search' in request.GET:
                word_result = find_lexeme_wordforms(word_search)
                return render(request, self.template_name, {'word_search': word_search,
                                                            'word_result': word_result, 'is_search': True})
            elif '_new_lexeme' in request.GET:
                language = request.GET['language']
                syntactic_category = request.GET['syntactic_category']
                spelling = request.GET['spelling']
                return redirect(reverse('wordengine:add_wordform_lexeme',
                                        kwargs={'language': language, 'syntactic_category': syntactic_category,
                                                'spelling': spelling}))
            else:
                lexeme = request.GET['chosen_lexeme']
                return redirect('wordengine:add_wordform', lexeme)


class ShowLexemeDetailsView(TemplateView):
    """Show details of lexeme view. Lexeme is indicated by spelling of a word"""

    template_name = 'wordengine/lexeme_details.html'

    def get(self, request, *args, **kwargs):
        given_lexeme = get_object_or_404(models.Lexeme, pk=kwargs.get('lexeme_id'))
        lexeme_words = given_lexeme.wordform_set.all()
        return render(request, self.template_name, {'given_lexeme': given_lexeme, 'lexeme_words': lexeme_words})


@login_required
@transaction.atomic
def delete_wordform(request, wordform_id):
    given_wordform = get_object_or_404(models.WordForm, pk=wordform_id)
    #TODO handle 404 for wordform
    taken_lexeme = given_wordform.lexeme
    #TODO handle non-existant lexeme
    source = models.Source.objects.get(pk=1)
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
        return redirect('wordengine:show_wordlist')
    else:
        return redirect('wordengine:show_lexemedetails', args=[taken_lexeme.id])

