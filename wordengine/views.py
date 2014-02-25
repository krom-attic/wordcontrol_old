from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from wordengine import forms, models


# Common functions here

def find_lexeme_wordforms(word_search):
    if word_search.is_valid():
        word_result = models.WordForm.objects.filter(spelling__istartswith=word_search.cleaned_data['spelling'])
        if word_search.cleaned_data['language']:
            word_result = word_result.filter(lexeme__language__exact=word_search.cleaned_data['language'])
        elif word_search.cleaned_data['syntactic_category']:
            word_result = word_result.filter(lexeme__syntactic_category__exact=
                                             word_search.cleaned_data['syntactic_category'])
    lexeme_result = models.Lexeme.objects.filter(id__in=word_result.values_list('lexeme', flat=True))
    #TODO Invalid search handling
    return word_result, lexeme_result


# Actual views here

def index(request):
    return render(request, 'wordengine/index.html')


class DoSmthWordFormView(TemplateView):
    """Sandbox view
    """

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


class AddWordFormView(TemplateView):
    """New word addition view
    """

    lexeme_form_class = forms.LexemeForm
    word_form_class = forms.WordFormForm
    source_form_class = forms.SourceSelectForm
    template_name = 'wordengine/word_add.html'

    def __init__(self, **kwargs):
        self.word_form = self.word_form_class()
        self.source_form = self.source_form_class()
        super(AddWordFormView, self).__init__(**kwargs)

    def __prefilter(self, filters):
        if filters['lang']:
            lang_filter = Q(language=filters['lang']) | Q(language=None)
            self.source_form.fields['source'].queryset = models.Source.objects.filter(lang_filter)
            self.word_form.fields['writing_system'].queryset = models.WritingSystem.objects.filter(lang_filter)
            self.word_form.fields['dialect_multi'].queryset = models.Dialect.objects.filter(lang_filter)

        if filters['synt_cat']:
            synt_cat_filter = Q(syntactic_category=filters['synt_cat']) | Q(syntactic_category=None)
            self.word_form.fields['gramm_category_set'].queryset = models.GrammCategorySet.objects.filter(synt_cat_filter)
            #TODO Correct this after gramm cat becomes language dependent

    def get(self, request, *args, **kwargs):
        self.source_form = self.source_form_class()
        try:
            given_lexeme = models.Lexeme.objects.get(pk=kwargs['lexeme_id'])
            self.word_form = self.word_form_class()
            self.__prefilter({'lang': given_lexeme.language, 'synt_cat': given_lexeme.syntactic_category})
            return render(request, self.template_name, {'given_lexeme': given_lexeme,
                                                        'word_form': self.word_form,
                                                        'source_form': self.source_form})
        except KeyError:
            lexeme_form = self.lexeme_form_class(initial={'language': kwargs['language'],
                                                          'syntactic_category': kwargs['syntactic_category']})
            self.word_form = self.word_form_class(initial={'spelling': kwargs['spelling']})
            self.__prefilter({'lang': kwargs['language'], 'synt_cat': kwargs['syntactic_category']})
            return render(request, self.template_name, {'word_form': self.word_form,
                                                        'lexeme_form': lexeme_form,
                                                        'source_form': self.source_form})

    def post(self, request, *args, **kwargs):
        self.word_form = self.word_form_class()
        is_saved = False
        lexeme_validated = 0
        if 'lexeme' in request.POST:
            lexeme = models.Lexeme.objects.get(pk=request.POST['lexeme'])
            lexeme_validated = 1
        else:
            lexeme_form = self.lexeme_form_class(request.POST)
            if lexeme_form.is_valid():
                lexeme_validated = 2
        self.source_form = self.source_form_class(request.POST)

        if lexeme_validated > 0 and self.source_form.is_valid():
            if lexeme_validated == 2:
                lexeme = lexeme_form.save()
            source = self.source_form.cleaned_data['source']
            change = models.DictChange(source=source, user_changer=request.user)
            change.save()
            word_form_initial = models.WordForm(lexeme=lexeme, dict_change_commit=change)
            self.word_form = self.word_form_class(request.POST, instance=word_form_initial)
            if self.word_form.is_valid():
                self.word_form.save()
                is_saved = True

        if (not is_saved) or ('_continue_edit' in request.POST):
            if lexeme_validated == 1:
                self.__prefilter({'lang': lexeme.language, 'synt_cat': lexeme.syntactic_category})
                return render(request, self.template_name, {'word_form': self.word_form, 'given_lexeme': lexeme,
                                                            'source_form': self.source_form})
            else:
                self.__prefilter({'lang': request.POST['language'], 'synt_cat': request.POST['syntactic_category']})
                return render(request, self.template_name, {'word_form': self.word_form, 'lexeme_form': lexeme_form,
                                                            'source_form': self.source_form})

        if '_add_new' in request.POST:
            return redirect('wordengine:add_wordform_lexeme')
        elif '_add_wordform' in request.POST:
            return redirect('wordengine:add_wordform', lexeme.id)
        else:
            return redirect('wordengine:show_lexemedetails', lexeme.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordFormView, self).dispatch(*args, **kwargs)


class ShowLexemeListView(TemplateView):
    """Show a list of wordfomrs view
    """

    word_search_form_class = forms.SearchWordFormForm
    template_name = 'wordengine/lexeme_list.html'

    def get(self, request, *args, **kwargs):
        if not request.GET:
            return render(request, self.template_name, {'word_search': self.word_search_form_class(),
                                                        'is_search': False})
        else:
            word_search = self.word_search_form_class(request.GET)
            if '_lexeme_search' in request.GET:
                word_result, lexeme_result = find_lexeme_wordforms(word_search)
                all_lexeme_words = models.WordForm.objects.filter(lexeme__in=lexeme_result)
                #TODO Here should go composition of lexeme cards, taking into account found and deleted wordforms
                return render(request, self.template_name, {'word_search': word_search, 'lexeme_result': lexeme_result,
                                                            'word_result': word_result, 'is_search': True})
            elif '_translation_search' in request.GET:
                pass

            elif '_new_lexeme' in request.GET:
                language = request.GET['language'] #TODO Replace these with word_search parsing
                syntactic_category = request.GET['syntactic_category']
                spelling = request.GET['spelling']
                return redirect(reverse('wordengine:add_wordform_lexeme',
                                        kwargs={'language': language, 'syntactic_category': syntactic_category,
                                                'spelling': spelling}))  # Kwargs are not passed w/o reverse???
            elif '_add_translation' in request.GET:
                pass
            else:
                lexeme_id = request.GET['_add_wordform']
                return redirect('wordengine:add_wordform', lexeme_id)


class ShowLexemeDetailsView(TemplateView):
    """Show details of lexeme view. Lexeme is indicated by spelling of a word
    """

    template_name = 'wordengine/lexeme_details.html'

    def get(self, request, *args, **kwargs):
        given_lexeme = get_object_or_404(models.Lexeme, pk=kwargs['lexeme_id'])
        lexeme_words = given_lexeme.wordform_set.all()
        if not request.GET:
            return render(request, self.template_name, {'given_lexeme': given_lexeme, 'lexeme_words': lexeme_words})
        else:
            try:
                lexeme_id = request.GET['_add_word']
                return redirect('wordengine:add_wordform', lexeme_id)
            except KeyError:
                lexeme_id = request.GET['_add_translation']
                return redirect('wordengine:add_translation', lexeme_id)


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
        return redirect('wordengine:show_lexemedetails', taken_lexeme.id)


class AddTranslationView(TemplateView):
    """ Class view for translation addition
    """

    #translation_class = forms.TraslationForm

    def get(self, request, *args, **kwargs):
        try:
            first_lexeme = models.Lexeme.objects.get(pk=kwargs['lexeme_id'])
            #TODO Display the lexeme
        except KeyError:
            pass

    def post(self, request, *args, **kwargs):
        translation = self.translation_class()
        is_saved = False
        pass
