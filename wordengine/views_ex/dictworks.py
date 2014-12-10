from wordengine import models
from collections import defaultdict
from django.db import transaction
from wordengine.specials.csvworks import parse_csv
from django.contrib.auth.decorators import login_required

# Common functions here


def find_lexemes_wordforms(word_search, exact):
    """
    For given search criteria returns matched lexemes among with matched wordform spellings
    """

    if word_search.is_valid():
        spelling = word_search.cleaned_data['spelling']
        language = word_search.cleaned_data['language']
        synt_cat = word_search.cleaned_data['syntactic_category']
        gramm_category = word_search.cleaned_data['gramm_category']
        source = word_search.cleaned_data['source']
        dialect = word_search.cleaned_data['dialect']
        writing_system = None

        if exact:
            word_result = models.WordformSpell.objects.filter(spelling__iexact=spelling)
        else:
            word_result = models.WordformSpell.objects.filter(spelling__istartswith=spelling)

        if gramm_category:
            word_result = word_result.filter(wordform__gramm_category_set=gramm_category)
        if source:
            word_result = word_result.filter(wordform__source_m=source)
        if dialect:
            word_result = word_result.filter(wordform__dialect_m=dialect)
        if language:
            word_result = word_result.filter(wordform__lexeme__language=language)
        if synt_cat:
            word_result = word_result.filter(wordform__lexeme__syntactic_category=synt_cat)

        temp_lexeme_result = defaultdict(list)

        for word in word_result:
            temp_lexeme_result[word.wordform.lexeme].append(word)
        lexeme_result = dict(temp_lexeme_result)  # Django bug workaround (#16335 marked as fixed, but it doesn't)

        return lexeme_result

    else:
        # TODO Add error message
        return {}


def find_translations(lexemes):

    translation_result = dict()

    for lexeme in lexemes:
        # This is a workaround for non-symmetric relation (it isn't possible with "through")
        translation_list = []
        for translation in models.Translation.objects.filter(lexeme_1=lexeme):
            translation_list.append(translation.lexeme_2)
        for translation in models.Translation.objects.filter(lexeme_2=lexeme):
            translation_list.append(translation.lexeme_1)
        translation_result[lexeme] = translation_list
        # If symmetric relations will be possible with "through", it should read:
        # translation_list = lexeme.translation_m.all()

    return translation_result


def parse_upload(request):

    transaction.set_autocommit(False)
    project = parse_csv(request)
    project.fill_project_dict()
    if project.errors:
        transaction.rollback()
    transaction.set_autocommit(True)

    return project.id, project.errors


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
        return redirect('wordengine:show_wordlist', taken_lexeme.id)