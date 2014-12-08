from wordengine import models
from collections import defaultdict
from django.db import transaction
from wordengine.specials.csvworks import parse_csv

# Common functions here


def find_lexemes_wordforms(word_search, exact):
    """
    For given search criteria returns matched lexemes among with matched wordform spellings
    """

    if word_search.is_valid():
        spelling = word_search.cleaned_data['spelling']
        language = word_search.cleaned_data['language']
        synt_cat = word_search.cleaned_data['syntactic_category']
        gramm_cats = []
        sources = []
        dialects = []
        writing_system = None

        if exact:
            word_result = models.WordformSpell.objects.filter(spelling__iexact=spelling)
        else:
            word_result = models.WordformSpell.objects.filter(spelling__istartswith=spelling)

        if language:
            word_result = word_result.filter(wordform__lexeme__language__exact=language)
        if synt_cat:
            word_result = word_result.filter(wordform__lexeme__syntactic_category__exact=synt_cat)
        if gramm_cats:
            pass  # TODO Filter by grammatical category
        if sources:
            pass  # TODO Filter by source
        if dialects:
            pass  # TODO Filter by dialect
        if writing_system:
            pass  # TODO Filter by writing system

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
        translation_list = []
        for translation in models.Translation.objects.filter(lexeme_1=lexeme):
            translation_list.append(translation.lexeme_2)
        for translation in models.Translation.objects.filter(lexeme_2=lexeme):
            translation_list.append(translation.lexeme_1)
        translation_result[lexeme] = translation_list

    return translation_result


def parse_upload(request):

    transaction.set_autocommit(False)
    project = parse_csv(request)
    project.fill_project_dict()
    if project.errors:
        transaction.rollback()
    transaction.set_autocommit(True)

    return project.id, project.errors