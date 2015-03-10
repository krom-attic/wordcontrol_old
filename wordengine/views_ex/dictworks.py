import datetime

from django.db import transaction
from django.contrib.auth.decorators import login_required

from wordengine import models
from wordengine.specials import csvworks


# Common functions here


class SearchDetails():

    def __init__(self):
        self.found_forms = set()
        self.translations_fetched = False

    def __str__(self):
        return ' '.join([str(self.found_forms), str(self.translations_fetched)])


def find_translations(lexeme):
    # TODO Numbering of Lexemes and SemanticCategories in Translations are swapped

    translation_result = {}
    # This is a workaround for non-symmetric relation (it isn't possible with "through")
    for translation in models.Translation.objects.filter(lexeme_1=lexeme):
        translation_result.setdefault(translation.lexeme_2.language, {}).\
            setdefault(translation.semantic_group_1, set()).add(translation.lexeme_2)
    for translation in models.Translation.objects.filter(lexeme_2=lexeme):
        translation_result.setdefault(translation.lexeme_1.language, {}).\
            setdefault(translation.semantic_group_2, set()).add(translation.lexeme_1)

    return translation_result


def find_lexemes_wordforms(word_search, exact, with_translations=False):
    """
    For given search criteria returns matched lexemes among with matched wordform spellings
    """

    if word_search.is_valid():
        lexeme_result = dict()

        spelling = word_search.cleaned_data['spelling'].strip()
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

        for word in word_result:
            lexeme = word.wordform.lexeme

            lexeme_result.setdefault(lexeme.syntactic_category, {}).setdefault(lexeme.language, {}).\
                setdefault(lexeme, SearchDetails()).found_forms.add(word.spelling)

            current_lexeme_details = lexeme_result[lexeme.syntactic_category][lexeme.language][lexeme]

            if not current_lexeme_details.translations_fetched and with_translations:
                current_lexeme_details.translations = find_translations(lexeme)

        return lexeme_result

    else:
        # TODO Add error message
        return {}


def parse_upload(request):
    transaction.set_autocommit(False)

    project = models.Project(user_uploader=request.user, timestamp_upload=datetime.datetime.now(),  # Always use UTC
                             filename=request.FILES['file'].name, source_id=request.POST['source'])
    csv_file = csvworks.get_csv(request.FILES['file'])
    project = csvworks.parse_csv(csv_file, project)

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