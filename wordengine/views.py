from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from wordengine import forms
from wordengine.dictworks import *

# Actual views here

def index(request):
    return redirect('wordengine:show_wordlist')


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


class AddWordformView(TemplateView):
    """New word addition view
    """

    lexeme_form_class = forms.LexemeForm
    wordform_form_class = forms.WordformForm
    template_name = 'wordengine/word_add.html'

    def __init__(self, **kwargs):
        # Makes these forms global and thus available for filtering
        self.wordform_form = self.wordform_form_class()
        super(AddWordformView, self).__init__(**kwargs)

    def _prefilter(self, filters):
        if filters['synt_cat']:
            synt_cat_filter = Q(syntactic_category=filters['synt_cat']) | Q(syntactic_category=None)
            self.wordform_form.fields['gramm_category_set'].queryset = models.GrammCategorySet.objects.filter(synt_cat_filter)

        if filters['language']:
            language_filter = Q(language=filters['language']) | Q(language=None)
            self.wordform_form.fields['source'].queryset = models.Source.objects.filter(language_filter)
            self.wordform_form.fields['writing_system'].queryset = models.WritingSystem.objects.filter(language_filter)
            self.wordform_form.fields['dialect_multi'].queryset = models.Dialect.objects.filter(language_filter)
            self.wordform_form.fields['gramm_category_set'].queryset =\
                self.wordform_form.fields['gramm_category_set'].queryset.filter(language_filter).order_by('position')
            # If position null is sorted before any position. Maybe a fix must be introduced

    def get(self, request, *args, **kwargs):
        try:
            self.wordform_form = self.wordform_form_class(initial={'spelling': kwargs['spelling']})
        except KeyError:
            self.wordform_form = self.wordform_form_class()

        try:
            given_lexeme = get_object_or_404(models.Lexeme, pk=kwargs['lexeme_id'])
            self._prefilter({'language': given_lexeme.language, 'synt_cat': given_lexeme.syntactic_category})
            return render(request, self.template_name, {'given_lexeme': given_lexeme,
                                                        'wordform_form': self.wordform_form})
        except KeyError:
            try:
                lexeme_form = self.lexeme_form_class(initial={'language': kwargs['language'],
                                                              'syntactic_category': kwargs['syntactic_category']})
                self._prefilter({'language': kwargs['language'], 'synt_cat': kwargs['syntactic_category']})
            except KeyError:
                lexeme_form = self.lexeme_form_class()
            try:
                first_lexeme = get_object_or_404(models.Lexeme, pk=kwargs['first_lexeme_id'])
            except KeyError:
                first_lexeme = None
            return render(request, self.template_name, {'wordform_form': self.wordform_form,
                                                        'lexeme_form': lexeme_form,
                                                        'first_lexeme': first_lexeme})

    def post(self, request, *args, **kwargs):
        is_saved = False
        lexeme_validated = 0
        try:
            lexeme = models.Lexeme.objects.get(pk=request.POST['lexeme'])
            lexeme_validated = 1
        except KeyError:
            lexeme_form = self.lexeme_form_class(request.POST)
            if lexeme_form.is_valid():
                lexeme_validated = 2

        if lexeme_validated > 0:
            transaction.set_autocommit(False)
            try:
                if lexeme_validated == 2:
                    lexeme = lexeme_form.save()
                wordform_form_initial = models.Wordform(lexeme=lexeme)
                self.wordform_form = self.wordform_form_class(request.POST, instance=wordform_form_initial)
                if self.wordform_form.is_valid():
                    wordform = self.wordform_form.save()
                    dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
                                                    object_id=wordform.id)
                    dict_change.save()
                    messages.success(request, "The word has been added")
                    is_saved = True
            finally:
                if not is_saved:
                    transaction.rollback()
                transaction.set_autocommit(True)
        else:
            self.wordform_form = self.wordform_form_class(request.POST)  # takes wordform from post if skipped this step above

        if (not is_saved) or ('_continue_edit' in request.POST):  # _continue_edit isn't used right now
            messages.warning(request, "The word hasn't been added")
            if lexeme_validated == 1:
                self._prefilter({'language': lexeme.language, 'synt_cat': lexeme.syntactic_category})
                return render(request, self.template_name, {'wordform_form': self.wordform_form, 'given_lexeme': lexeme})
            else:
                self._prefilter({'language': request.POST['language'], 'synt_cat': request.POST['syntactic_category']})
                return render(request, self.template_name, {'wordform_form': self.wordform_form, 'lexeme_form': lexeme_form})

        if '_add_new' in request.POST:
            return redirect('wordengine:add_wordform_lexeme')
        elif '_add_wordform' in request.POST:
            return redirect('wordengine:add_wordform', lexeme.id)
        elif '_add_translation' in request.POST:
            return redirect('wordengine:add_translation', lexeme.id)
        elif '_goto_translation' in request.POST:
            first_lexeme = models.Lexeme.objects.get(pk=request.POST['first_lexeme'])
            return redirect('wordengine:add_translation', first_lexeme.id, lexeme.id)
        else:
            return redirect('wordengine:show_lexemedetails', lexeme.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordformView, self).dispatch(*args, **kwargs)


class ShowLexemeListView(TemplateView):
    """Show a list of lexemes
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
                                                            'translation_search': 'word_search'})
            elif '_lexeme_details' in request.GET:
                given_lexeme = get_object_or_404(models.Lexeme, pk=request.GET['_lexeme_details'])
                lexeme_words = given_lexeme.wordform_set.all()
                return render(request, self.template_name, {'word_search_form': word_search_form,
                                                            'given_lexeme': given_lexeme, 'lexeme_words': lexeme_words})
            elif '_find_translation' in request.GET:  # combines both of above
                lexeme_result = get_object_or_404(models.Lexeme, pk=request.GET['_find_translation'])
                lexeme_words = lexeme_result.wordform_set.all()
                translation_result = find_lexeme_translations([lexeme_result])
                return render(request, self.template_name, {'word_search_form': word_search_form,
                                                            'given_lexeme': lexeme_result, 'lexeme_words': lexeme_words,
                                                            'translation_result': translation_result,
                                                            'translation_search': 'exact_lexeme'})
            elif '_new_lexeme' in request.GET:
                language = request.GET['language']
                syntactic_category = request.GET['syntactic_category']
                spelling = request.GET['spelling']
                return redirect('wordengine:add_wordform_lexeme', language=language,
                                syntactic_category=syntactic_category,  spelling=spelling)
            elif '_add_translation' in request.GET:
                lexeme_id = request.GET['_add_translation']
                return redirect('wordengine:add_translation', lexeme_id)
            elif '_add_wordform' in request.GET:
                lexeme_id = request.GET['_add_wordform']
                return redirect('wordengine:add_wordform', lexeme_id)

            else:
                messages.error(request, "Invalid request")
                return render(request, self.template_name, {'word_search_form': word_search_form})


@login_required
@transaction.atomic
def delete_wordform(request, wordform_id):

    given_wordform = get_object_or_404(models.Wordform, pk=wordform_id)
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

    def __init__(self, **kwargs):
        # Makes these forms global and thus available for filtering
        self.translation_form = self.translation_form_class()
        super(AddTranslationView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        # TODO Second lexeme's parameters must match those of first
        try:
            first_lexeme = get_object_or_404(models.Lexeme, pk=kwargs['lexeme_id'])
        except KeyError:
            pass  # TODO Handle "no first lexeme" error

        if '_lexeme_search' in request.GET:
            word_search_form = self.word_search_form_class(request.GET)
            lexeme_result = find_lexeme_wordforms(word_search_form, False)
            return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                        'word_search_form': word_search_form,
                                                        'lexeme_result': lexeme_result,
                                                        'searchtype': 'in_translation'})

        if '_new_lexeme' in request.GET:
            language = request.GET['language']
            syntactic_category = request.GET['syntactic_category']
            spelling = request.GET['spelling']
            return redirect('wordengine:add_wordform_lexeme', language=language,
                            syntactic_category=syntactic_category,  spelling=spelling,
                            first_lexeme_id=first_lexeme.id)

        if '_add_as_translation' in request.GET:
            second_lexeme = get_object_or_404(models.Lexeme, pk=request.GET['_add_as_translation'])
            return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                        'second_lexeme': second_lexeme,
                                                        'translation_form': self.translation_form})

        else:
            try:
                second_lexeme = get_object_or_404(models.Lexeme, pk=kwargs['second_lexeme_id'])
                return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                            'second_lexeme': second_lexeme,
                                                            'translation_form': self.translation_form})
            except KeyError:
                word_search_form = self.word_search_form_class(initial={'syntactic_category': first_lexeme.syntactic_category})
                return render(request, self.template_name, {'first_lexeme': first_lexeme,
                                                            'word_search_form': word_search_form})



    def post(self, request, *args, **kwargs):
        is_saved = False
        lexeme_1 = models.Lexeme.objects.get(pk=request.POST['lexeme_1'])
        lexeme_2 = models.Lexeme.objects.get(pk=request.POST['lexeme_2'])
        if lexeme_1.language.term_full < lexeme_2.language.term_full:
            lexeme_1, lexeme_2 = lexeme_2, lexeme_1
        translation_initial = models.Translation(lexeme_1=lexeme_1, lexeme_2=lexeme_2)
        self.translation_form = self.translation_form_class(request.POST, instance=translation_initial)
        if self.translation_form.is_valid():
            translation = self.translation_form.save()
            dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
                                            object_id=translation.id)
            dict_change.save()
            is_saved = True

        if is_saved:
            messages.success(request, "The word has been added")
            return redirect('wordengine:index')  # TODO Add sensible redirect

        else:
            messages.warning(request, "The word hasn't been added")
            # TODO Add sensible redirect


class AdminView(TemplateView):
    """ Class view for admin panel
    """

    template_name = 'wordengine/admin.html'
    admin_form_class = forms.AdminForm

    def get(self, request, *args, **kwargs):
        admin_form = self.admin_form_class(request.GET)
        if '_language_setup' in request.GET:
            language = request.GET['language']
            return redirect('wordengine:language_setup', language)
        else:
            return render(request, self.template_name, {'admin_form': admin_form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminView, self).dispatch(*args, **kwargs)


class LanguageSetupView(TemplateView):
    """ Class view for language setup
    """

    template_name = 'wordengine/language_setup.html'
    language_form_class = forms.LanguageSetupForm
    grcatsetorder_form_class = forms.GrammCategorySetForm

    def get(self, request, *args, **kwargs):
        given_language = get_object_or_404(models.Language, pk=kwargs['language_id'])
        language_form = self.language_form_class(instance=given_language)
        grcatsets = get_list_or_404(models.GrammCategorySet, language=given_language)
        grcatset_forms = {}
        for grcatset in grcatsets:
            grcatset_forms[grcatset.id] = self.grcatsetorder_form_class(instance=grcatset)

        return render(request, self.template_name, {'language_form': language_form, 'grcatset_forms': grcatset_forms})

    def post(self, request, *args, **kwargs):
        given_language = get_object_or_404(models.Language, pk=kwargs['language_id'])
        language_form = self.language_form_class(request.POST, instance=given_language)
       # TODO Add function to add gramm cat sets to the language
  #      try:
  #          for existing_grcatset in get_list_or_404(models.GrammCategorySetLanguageOrder, language=given_language):
#                existing_grcatset.delete()
#        except ObjectDoesNotExist:
#            pass
#        for grcatset_id in request.POST.getlist('gramm_category_set'):
#            grcatset = models.GrammCategorySet.objects.get(pk=grcatset_id)
#            position = request.POST.getlist('position')[request.POST.getlist('gramm_category_set').index(grcatset_id)]
#            if position != '-1':
#                grcatset_pos = models.GrammCategorySetLanguageOrder(language=given_language, gramm_category_set=grcatset,
 #                                                                   position=position)
                #grcatset_pos.save()
        language_form.save()  # TODO Add messages
        return render(request, self.template_name, {'language_form': language_form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LanguageSetupView, self).dispatch(*args, **kwargs)



class DictionaryDataImportView(TemplateView):
    """ Class view for importing dictionary data via file upload
    """

    template_name = 'wordengine/data_import.html'
    upload_form_class = forms.UploadFileForm

    def get(self, request, *args, **kwargs):
        upload_form = self.upload_form_class()
        return render(request, self.template_name, {'upload_form': upload_form})

    def post(self, request, *args, **kwargs):
        upload_form = self.upload_form_class(request.POST, request.FILES)
        if upload_form.is_valid():
            parse_data_import(request.FILES['file'])
            upload_form = self.upload_form_class()
        return render(request, self.template_name, {'upload_form': upload_form})
