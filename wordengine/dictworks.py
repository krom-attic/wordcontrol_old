from wordengine import models
from collections import defaultdict
import csv
import re
import codecs
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist


# Common functions here

def find_lexemes_wordforms(word_search, exact):

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
    lexeme_result = dict(temp_lexeme_result)  # Django bug workaround (#16335 marked as fixed, but it doesn't)
    #TODO Invalid search handling
    return lexeme_result


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


def modsave(request, upd_object, upd_fields):

    field_change = dict()
    for upd_field in upd_fields.keys():
        field_change[upd_field] = models.FieldChange(user_changer=request.user,
                                                     object_type=type(upd_object).__name__,
                                                     object_id=upd_object.id, field_name=upd_field,
                                                     old_value=getattr(upd_object, upd_field))
        setattr(upd_object, upd_field, upd_fields.get(upd_field))
    upd_object.save()
    for upd_field in field_change.keys():
        field_change[upd_field].new_value = getattr(upd_object, upd_field)
        field_change[upd_field].save()


def parse_data_import(request):
    """
    @param uploaded_file:
    @return:

    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """

    # TODO Wrap with manual commit

    language_source = models.Language.objects.get(pk=request.POST['language_1'])
    language_target = (models.Language.objects.get(pk=request.POST['language_2']),
                       models.Language.objects.get(pk=request.POST['language_2']),
                       models.Language.objects.get(pk=request.POST['language_2']))  # TODO Should get real languages
    source_translation = models.Source.objects.get(pk=request.POST['source_translation'])
    WORD_SOURCES = {0: None, 1: source_translation}
    LANG_SRC_COLS = ('lang_src1', 'lang_src2',)  # TODO Unhardcode this
    LANG_TRGT_COLS = ('lang_trgt1', 'lang_trgt2',)  # TODO Unhardcode this
    COLS = ('lex_param',) + LANG_SRC_COLS + LANG_TRGT_COLS + ('comment',)
    source_1 = WORD_SOURCES.get(request.POST['source_1'])
    source_2 = WORD_SOURCES.get(request.POST['source_2'])
    # TODO Здесь нужно получить перечень систем письма и диалектов для каждого столбца
    # try:
    #     writing_system = models.WritingSystem.objects.get(pk=request.POST['writing_system_???'])
    # except ValueError:
    #     writing_system = None
    writing_system_stub = models.WritingSystem.objects.get(pk=1)
#     try:
#         dialect_default = models.Dialect.objects.get(pk=request.POST['dialect_default_???'])
#     except ValueError:
#         dialect_default = None

    transaction.set_autocommit(False)

    added_translations = []

    csvreader = csv.DictReader(codecs.iterdecode(request.FILES['file'], 'utf-8'), fieldnames=COLS,
                               dialect=csv.excel_tab, delimiter='\t')

    for n, row in enumerate(csvreader):
        if n == 0:
            continue
        if row.get('lex_param'):  # Check if a new lexeme is in the row
            lex_param = row.get('lex_param').split('[')
            # synt_cat = models.SyntacticCategory.objects.get(term_abbr=lex_param[0])
            synt_cat = models.SyntacticCategory.objects.get(pk=1)  # TODO Stub
            if len(lex_param) == 2:
                # inflection = models.Inflection.objects.get(value=lex_param[1])  # TODO Trim right bracket
                inflection = None
                print(lex_param[1])
            # TODO: if lex_param splits into more pieces -> smth went wrong
            lexeme_src = models.Lexeme(language=language_source, syntactic_category=synt_cat)
            # lexeme_src.save()
            print('row' + str(n))
            print(lex_param[0])
            print(lexeme_src)

            try:
                main_gr_cat_1 = models.GrammCategorySet.objects.filter(language=language_source,
                                                                       syntactic_category=synt_cat)\
                    .order_by('position').first()
            except ObjectDoesNotExist:
                main_gr_cat_1 = None

            for i, col in enumerate(LANG_SRC_COLS):
                lexeme_wordforms = row.get(col)
                for current_wordform in lexeme_wordforms.split('|'):  # TODO Handle empty line correctly
                    # TODO Here must split futher
                    wordform = models.Wordform(lexeme=lexeme_src, spelling=current_wordform, gramm_category_set=None,
                                               writing_system=writing_system_stub)
                    print('col: ' + col)
                    print(wordform)
                    # wordform.save()
                    # TODO Here add dialect and source
#                     if current_wordform[1]:
#                         dialect = models.Dialect.objects.get(term_abbr=current_wordform[1],  # TODO Add import error
#                                                              language=current_row_params[2][0].language)
#                     else:
#                         dialect = current_row_params[2][2]
#                     try:
#                         wordform.dialect_multi.add(dialect)
#                     except IntegrityError:
#                         pass  # Nothing to do if dialect isn't specified anywhere
#                     try:
#                         wordform.source.add(current_row_params[2][3])
#                     except IntegrityError:
#                         pass  # Nothing to do if source isn't specified anywhere
#                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                                     object_id=wordform.id)
#                     dict_change.save()


#  TODO  WTF vvvvv ?????
#         if lexeme_1.wordform_set.first():
#             current_wordforms = lexeme_1.wordform_set
#         else:
#             try:
#                 for wordform in current_wordforms.all():
#                     wordform.pk = None
#                     wordform.lexeme = lexeme_1
#                     wordform.save()
#             except UnboundLocalError:
#                 pass  # TODO Handle blank first wordform error
#         # Does it need to be saved after "add"?

        for i, col in enumerate(LANG_TRGT_COLS):  # Iterate through multiple target languages
            if row.get(col):
                print('col: ' + col)

                # TODO Split lexemes!!

                lexeme_trg = models.Lexeme(language=language_target[i],
                                           syntactic_category=synt_cat)
                # lexeme_trg.save()
                print(lexeme_trg)
                # try:
                #     main_gr_cat_2 = models.GrammCategorySet.objects.filter(language=language_target[i],
                #                                                            syntactic_category=synt_cat)\
                #         .order_by('position').first()
                # except ObjectDoesNotExist:
                #     main_gr_cat_2 = None

                relation = models.LexemeRelation(lexeme_1=lexeme_src, lexeme_2=lexeme_trg)
                # relation.save()

                semantic_group_src = models.SemanticGroup()  # TODO Here should split input
                semantic_group_trg = models.SemanticGroup()  # TODO Also add sources??

                # TODO Add persisent wordform link
                translation = models.Translation(lexeme_relation=relation, direction=1, semantic_group_1=semantic_group_src,
                                                 semantic_group_2=semantic_group_trg, is_visible=True)
                # translation.save()

                # translation.source.add(source_translation)

                # TODO Log every change - overload save() method?
                # dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
                #                                 object_id=translation.id)
                # dict_change.save()
                added_translations.append(translation)
                print(translation)
                # TODO Suggest translation constraint if marked in a csv
#
#     # TODO Add form for commenting and duplicates resolution
#
#
#
#
#     return added_translations