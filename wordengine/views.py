from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from wordengine import forms, models
from collections import defaultdict


# Common functions here

def find_lexeme_wordforms(word_search, exact):
    # AD 2014-04-09 - ok
    if word_search.is_valid():
        if exact:
            word_result = models.Wordform.objects.filter(spelling__iexact=word_search.cleaned_data['spelling'])
        else:
            word_result = models.Wordform.objects.filter(spelling__istartswith=word_search.cleaned_data['spelling'])
        if word_search.cleaned_data['language']:
            word_result = word_result.filter(lexeme__language__exact=word_search.cleaned_data['language'])
        elif word_search.cleaned_data['syntactic_category']:
            word_result = word_result.filter(lexeme__syntactic_category__exact=
                                             word_search.cleaned_data['syntactic_category'])
    temp_lexeme_result = defaultdict(list)
    for word in word_result:
        temp_lexeme_result[word.lexeme].append(word)
    lexeme_result = dict(temp_lexeme_result)  # Django bug workaround (#16335 marked as fixed, but seems doesn't)
    #TODO Invalid search handling
    return lexeme_result


def find_lexeme_translations(lexemes):
    # AD 2014-04-09 - ok
    translation_result = dict()

    for lexeme in lexemes:
        translation_list = []
        for translation in models.Translation.objects.filter(lexeme_1=lexeme):
            translation_list.append(translation.lexeme_2)
        for translation in models.Translation.objects.filter(lexeme_2=lexeme):
            translation_list.append(translation.lexeme_1)
        if len(translation_list) > 0:
            translation_result[lexeme] = translation_list

    return translation_result

# Actual views here

def index(request):
    return render(request, 'wordengine/index.html')


class DoSmthWordformView(TemplateView):
    """Sandbox view
    """

    some_object_class = forms.DoSmthWithIdForm
    template_name = 'wordengine/do_smth.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'smth_form': self.some_object_class()})

    def post(self, request, *args, **kwargs):
        if '_restore_wordform' in request.POST:
            wordform_form = get_object_or_404(models.Wordform, pk=request.POST['given_id'])
            wordform_form.is_deleted = False
            wordform_form.save()
        return redirect('wordengine:action_result')


def addsave():
    # AD 2014-04-09 - ok

    deletion_record = dict()
    for upd_field in upd_fields.keys():
        deletion_record[upd_field] = models.FieldChange(user_changer=request.user,
                                                        object_type=upd_object.__class__.__name__,
                                                        object_id=upd_object.id, field_name=upd_field,
                                                        old_value=getattr(upd_object, upd_field))
        setattr(upd_object, upd_field, upd_fields.get(upd_field))
    upd_object.save()
    for upd_field in deletion_record.keys():
        deletion_record[upd_field].new_value = getattr(upd_object, upd_field)
        deletion_record[upd_field].save()


class AddWordformView(TemplateView):
    """New word addition view
    """
    # AD 2014-04-09 -

    lexeme_form_class = forms.LexemeForm
    wordform_form_class = forms.WordformForm
    source_form_class = forms.SourceSelectForm
    template_name = 'wordengine/word_add.html'

    def __init__(self, **kwargs):
        self.wordform_form = self.wordform_form_class()
        # TODO Does it needs to place here a lexeme_form?
        self.source_form = self.source_form_class()
        super(AddWordformView, self).__init__(**kwargs)

    def __prefilter(self, filters):
        if filters['lang']:
            lang_filter = Q(language=filters['lang']) | Q(language=None)
            self.source_form.fields['source'].queryset = models.Source.objects.filter(lang_filter)
            self.wordform_form.fields['writing_system'].queryset = models.WritingSystem.objects.filter(lang_filter)
            self.wordform_form.fields['dialect_multi'].queryset = models.Dialect.objects.filter(lang_filter)
            #TODO Add another filter after gramm cat set becomes language dependent

        if filters['synt_cat']:
            synt_cat_filter = Q(syntactic_category=filters['synt_cat']) | Q(syntactic_category=None)
            self.wordform_form.fields['gramm_category_set'].queryset = models.GrammCategorySet.objects.filter(synt_cat_filter)

    def get(self, request, *args, **kwargs):
        self.source_form = self.source_form_class()
        try:
            self.wordform_form = self.wordform_form_class(initial={'spelling': kwargs['spelling']})
        except KeyError:
            self.wordform_form = self.wordform_form_class()

        try:
            given_lexeme = models.Lexeme.objects.get(pk=kwargs['lexeme_id'])
            self.__prefilter({'lang': given_lexeme.language, 'synt_cat': given_lexeme.syntactic_category})
            return render(request, self.template_name, {'given_lexeme': given_lexeme,
                                                        'wordform_form': self.wordform_form,
                                                        'source_form': self.source_form})
        except KeyError:
            try:
                lexeme_form = self.lexeme_form_class(initial={'language': kwargs['language'],
                                                              'syntactic_category': kwargs['syntactic_category']})
                self.__prefilter({'lang': kwargs['language'], 'synt_cat': kwargs['syntactic_category']})
            except KeyError:
                lexeme_form = self.lexeme_form_class()
            return render(request, self.template_name, {'wordform_form': self.wordform_form,
                                                        'lexeme_form': lexeme_form,
                                                        'source_form': self.source_form})

    def post(self, request, *args, **kwargs):
        self.wordform_form = self.wordform_form_class()
        is_saved = False
        lexeme_validated = 0
        try:
            lexeme = models.Lexeme.objects.get(pk=request.POST['lexeme'])
            lexeme_validated = 1
        except KeyError:
            lexeme_form = self.lexeme_form_class(request.POST)
            if lexeme_form.is_valid():
                lexeme_validated = 2

        self.source_form = self.source_form_class(request.POST)

        if lexeme_validated > 0 and self.source_form.is_valid():
            transaction.set_autocommit(False)
            try:
                if lexeme_validated == 2:
                    lexeme = lexeme_form.save()
                wordform_form_initial = models.Wordform(lexeme=lexeme)
                self.wordform_form = self.wordform_form_class(request.POST, instance=wordform_form_initial)
                if self.wordform_form.is_valid():
                    wordform = self.wordform_form.save()
                    source = self.source_form.cleaned_data['source']
                    dict_change = models.DictChange(source=source, user_changer=request.user, object_type='Wordform',
                                                    object_id=wordform.id)
                    dict_change.save()
                    #transaction.commit()
                    messages.success(request, "The word has been added")
                    is_saved = True
                    #transaction.rollback()
                else:
                    transaction.rollback() # тут какая-то ерунда, коммит всё равно происходит. подумать!
            finally:
                transaction.set_autocommit(True)

        if (not is_saved) or ('_continue_edit' in request.POST):  # _continue_edit isn't used right now
            messages.warning(request, "The word hasn't been added")
            if lexeme_validated == 1:
                self.__prefilter({'lang': lexeme.language, 'synt_cat': lexeme.syntactic_category})
                return render(request, self.template_name, {'wordform_form': self.wordform_form, 'given_lexeme': lexeme,
                                                            'source_form': self.source_form})
            else:
                self.__prefilter({'lang': request.POST['language'], 'synt_cat': request.POST['syntactic_category']})
                return render(request, self.template_name, {'wordform_form': self.wordform_form, 'lexeme_form': lexeme_form,
                                                            'source_form': self.source_form})

        if '_add_new' in request.POST:
            return redirect('wordengine:add_wordform_lexeme')
        elif '_add_wordform' in request.POST:
            return redirect('wordengine:add_wordform', lexeme.id)
        elif '_add_translation' in request.POST:
            return redirect('wordengine:add_translation', lexeme.id)
        else:
            return redirect('wordengine:show_lexemedetails', lexeme.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordformView, self).dispatch(*args, **kwargs)


class ShowLexemeListView(TemplateView):
    # AD 2014-04-09 - ok
    """Show a list of wordfomrs view
    """

    word_search_form_class = forms.SearchWordformForm
    template_name = 'wordengine/lexeme_list.html'

    def get(self, request, *args, **kwargs):
        if not request.GET:
            return render(request, self.template_name, {'word_search_form': self.word_search_form_class()})
        else:
            word_search_form = self.word_search_form_class(request.GET)

            if '_lexeme_search' in request.GET:
                lexeme_result = find_lexeme_wordforms(word_search_form, False)
                return render(request, self.template_name, {'word_search_form': word_search_form,
                                                            'lexeme_result': lexeme_result, 'searchtype': 'regular'})
            elif '_translation_search' in request.GET:
                lexeme_result = find_lexeme_wordforms(word_search_form, True)
                translation_result = find_lexeme_translations(lexeme_result.keys())
                return render(request, self.template_name, {'word_search_form': word_search_form,
                                                            'translation_result': translation_result,
                                                            'translation_search': True})

            elif '_new_lexeme' in request.GET:
                language = request.GET['language']
                syntactic_category = request.GET['syntactic_category']
                spelling = request.GET['spelling']
                return redirect('wordengine:add_wordform_lexeme', language=language,
                                syntactic_category=syntactic_category,  spelling=spelling)
            elif '_add_translation' in request.GET:
                lexeme_id = request.GET['_add_translation']
                return redirect('wordengine:add_translation', lexeme_id)

            else:
                lexeme_id = request.GET['_add_wordform']
                return redirect('wordengine:add_wordform', lexeme_id)


class ShowLexemeDetailsView(TemplateView):
    # AD 2014-04-09 - ok

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


def modsave(request, upd_object, upd_fields):
    # AD 2014-04-09 - ok

    field_change = dict()
    for upd_field in upd_fields.keys():
        field_change[upd_field] = models.FieldChange(user_changer=request.user,
                                                        object_type=upd_object.__class__.__name__,
                                                        object_id=upd_object.id, field_name=upd_field,
                                                        old_value=getattr(upd_object, upd_field))
        setattr(upd_object, upd_field, upd_fields.get(upd_field))
    upd_object.save()
    for upd_field in field_change.keys():
        field_change[upd_field].new_value = getattr(upd_object, upd_field)
        field_change[upd_field].save()


@login_required
@transaction.atomic
def delete_wordform(request, wordform_id):
    # AD 2014-04-09 - ok

    given_wordform = get_object_or_404(models.Wordform, pk=wordform_id)
    #TODO replace 404 with error description
    taken_lexeme = given_wordform.lexeme

    if (taken_lexeme.wordform_set.count() == 1) and (taken_lexeme.translationbase_fst_set.count() +
                                                     taken_lexeme.translationbase_snd_set.count() > 0):
        messages.add_message(request, messages.ERROR, "The word has translations and thus can't be deleted")
    else:
        modsave(request, given_wordform, {'is_deleted': True})

        messages.add_message(request, messages.SUCCESS, "The word has been deleted")

    if taken_lexeme.wordform_set.filter(is_deleted__exact=False).count() == 0:
        return redirect('wordengine:show_wordlist')
    else:
        return redirect('wordengine:show_lexemedetails', taken_lexeme.id)


class AddTranslationView(TemplateView):
    """ Class view for translation addition
    """

    template_name = 'wordengine/translation_add.html'

    translation_form_class = forms.AddTranslationForm
    word_search_form_class = forms.SearchWordformForm
    source_form_class = forms.SourceSelectForm

    def __init__(self, **kwargs):
        self.source_form = self.source_form_class()
        self.translation_form = self.translation_form_class()
        super(AddTranslationView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        # TODO Second lexeme's parameters must match those of first
        try:
            first_lexeme = models.Lexeme.objects.get(pk=kwargs['lexeme_id'])

            if '_lexeme_search' in request.GET:
                word_search_form = self.word_search_form_class(request.GET)
                lexeme_result = find_lexeme_wordforms(word_search_form, False)
                return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                            'word_search_form': word_search_form,
                                                            'lexeme_result': lexeme_result,
                                                            'searchtype': 'in_translation'})

            if '_new_lexeme' in request.GET:
                pass

            if '_add_as_translation' in request.GET:
                second_lexeme = models.Lexeme.objects.get(pk=request.GET['_add_as_translation'])
                return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                            'second_lexeme': second_lexeme,
                                                            'translation_form': self.translation_form,
                                                            'source_form': self.source_form})

            else:
                word_search_form = self.word_search_form_class(request.GET)
                return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                            'word_search_form': word_search_form})

        except KeyError:
            pass  # TODO Handle "no first lexeme" error

    def post(self, request, *args, **kwargs):
        is_saved = False
        self.source_form = self.source_form_class(request.POST)
        if self.source_form.is_valid():
            source = self.source_form.cleaned_data['source']
            try:
                lexeme_1 = models.Lexeme.objects.get(pk=request.POST['lexeme_1'])
                lexeme_2 = models.Lexeme.objects.get(pk=request.POST['lexeme_2'])
                if lexeme_1.language.term_full < lexeme_2.language.term_full:
                    lexeme_1, lexeme_2 = lexeme_2, lexeme_1
            except KeyError:
                pass # TODO Handle an lexeme error
            change = models.DictChange(source=source, user_changer=request.user)
            change.save()
            translation_initial = models.Translation(lexeme_1=lexeme_1, lexeme_2=lexeme_2, dict_change_commit=change)
            self.translation_form = self.translation_form_class(request.POST, instance=translation_initial)
            if self.translation_form.is_valid():
                print(self.translation_form)
                self.translation_form.save()
                is_saved = True

        if is_saved:
            pass
            return redirect('wordengine:index')

        else:
            pass