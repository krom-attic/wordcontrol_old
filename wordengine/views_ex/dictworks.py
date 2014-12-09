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
        gramm_cat = word_search.cleaned_data['gramm_cat']
        source = word_search.cleaned_data['source']
        dialect = word_search.cleaned_data['dialect']
        writing_system = None

        if exact:
            word_result = models.WordformSpell.objects.filter(spelling__iexact=spelling)
        else:
            word_result = models.WordformSpell.objects.filter(spelling__istartswith=spelling)

        if language:
            word_result = word_result.filter(wordform__lexeme__language=language)
        if synt_cat:
            word_result = word_result.filter(wordform__lexeme__syntactic_category=synt_cat)
        if gramm_cat:
            word_result = word_result.filter(wordform__gramm_category_set=gramm_cat)
        if source:
            word_result = word_result.filter(wordform__source__in=source)
        if dialect:
            word_result = word_result.filter(wordform__dialect=dialect)
        if writing_system:
            word_result = word_result.filter(wordform__)

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