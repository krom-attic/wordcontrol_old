from wordengine import models
from collections import defaultdict
import csv
import io
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


def parse_data_import(uploaded_file):
    """
    @param uploaded_file:
    @return:

    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """

    # TODO Wrap with manual commit

    csvreader = csv.DictReader(codecs.iterdecode(uploaded_file, 'utf-16'), delimiter=';')
    for row in csvreader:
         print(row)

#     language_1 = models.Language.objects.get(pk=request.POST['language_1'])
#     language_2 = models.Language.objects.get(pk=request.POST['language_2'])
#     source_translation = models.Source.objects.get(pk=request.POST['source_translation'])
#     WORD_SOURCES = {0: None, 1: source_translation}
#       # TODO Fix field name hardcode
#     ROW_CAPTIONS = {'spell1': 'Написание 1', 'transcr1': 'Произношение 1', 'synt_cat': 'Часть речи', 'spell2':
#                     'Написание 2', 'transcr2': 'Произношение 2', 'transl_constr': 'Ограничение перевода'}
#     source_1 = WORD_SOURCES.get(request.POST['source_1'])
#     source_2 = WORD_SOURCES.get(request.POST['source_2'])
#     try:
#         writing_system_orth_1 = models.WritingSystem.objects.get(pk=request.POST['writing_system_orth_1'])
#     except ValueError:
#         writing_system_orth_1 = None
#     try:
#         writing_system_phon_1 = models.WritingSystem.objects.get(pk=request.POST['writing_system_phon_1'])
#     except ValueError:
#         writing_system_phon_1 = None
#     try:
#         writing_system_orth_2 = models.WritingSystem.objects.get(pk=request.POST['writing_system_orth_2'])
#     except ValueError:
#         writing_system_orth_2 = None
#     try:
#         writing_system_phon_2 = models.WritingSystem.objects.get(pk=request.POST['writing_system_phon_2'])
#     except ValueError:
#         writing_system_phon_2 = None
#     try:
#         dialect_1_default = models.Dialect.objects.get(pk=request.POST['dialect_1_default'])
#     except ValueError:
#         dialect_1_default = None
#     try:
#         dialect_2_default = models.Dialect.objects.get(pk=request.POST['dialect_2_default'])
#     except ValueError:
#         dialect_2_default = None
#
#     transaction.set_autocommit(False)
#
#     added_translations = []
#
#     for row in reader:  # Split larger files by chunks?
#         if row.get(ROW_CAPTIONS['synt_cat']):
#             synt_cat = models.SyntacticCategory.objects.get(term_abbr=row.get(ROW_CAPTIONS['synt_cat']))
#
#             lexeme_1 = models.Lexeme(language=language_1, syntactic_category=synt_cat)
#             lexeme_1.save()
#             # print(models.Lexeme.objects.filter(pk=lexeme_1.id).values())
#
#             try:
#                 main_gr_cat_1 = models.GrammCategorySet.objects.filter(language=language_1,
#                                                                        syntactic_category=synt_cat)\
#                     .order_by('position').first()
#             except ObjectDoesNotExist:
#                 main_gr_cat_1 = None
#
#             # print(main_gr_cat_1)
#
#         if row.get(ROW_CAPTIONS['spell2']) or row.get(ROW_CAPTIONS['transcr2']):
#             lexeme_2 = models.Lexeme(language=language_2, syntactic_category=synt_cat)  # TODO Add import error
#             lexeme_2.save()
#             # print(models.Lexeme.objects.filter(pk=lexeme_2.id).values())
#
#             try:
#                 main_gr_cat_2 = models.GrammCategorySet.objects.filter(language=language_2,
#                                                                        syntactic_category=synt_cat)\
#                     .order_by('position').first()
#
#             except ObjectDoesNotExist:
#                 main_gr_cat_2 = None
#
#             # print(main_gr_cat_2)
#
#             # TR REF START
#             translation = models.Translation(lexeme_1=lexeme_1, lexeme_2=lexeme_2)
#             translation.save()
#             translation.source.add(source_translation)
#             dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
#                                             object_id=translation.id)
#             dict_change.save()
#             # TR REF FINISH
#             added_translations.append(translation)
#             # print(models.Translation.objects.filter(pk=translation.id).values())
#
#
#         WORDFORM_PARAMS = (
#             (lexeme_1, main_gr_cat_1, dialect_1_default, source_1),
#             (lexeme_2, main_gr_cat_2, dialect_2_default, source_2),
#         )
#
#         ROW_GET_PARAMS = (
#             (ROW_CAPTIONS['spell1'], writing_system_orth_1, WORDFORM_PARAMS[0]),
#             (ROW_CAPTIONS['transcr1'], writing_system_phon_1, WORDFORM_PARAMS[0]),
#             (ROW_CAPTIONS['spell2'], writing_system_orth_2, WORDFORM_PARAMS[1]),
#             (ROW_CAPTIONS['transcr2'], writing_system_phon_2, WORDFORM_PARAMS[1]),
#         )
#
#         for current_row_params in ROW_GET_PARAMS:
#             current_row_wordform = row.get(current_row_params[0])
#             if current_row_wordform:
#                 for current_wordform in current_row_wordform.split(' | '):
#                     current_wordform = current_wordform.split(' (')  # TODO Check whether only 2 parts generated
#                     try:
#                         current_wordform[1] = current_wordform[1].rstrip(')')
#                     except IndexError:
#                         current_wordform.append(None)
#                     wordform = models.Wordform(lexeme=current_row_params[2][0], spelling=current_wordform[0],
#                                                        gramm_category_set=current_row_params[2][1],
#                                                        writing_system=current_row_params[1])
#                     wordform.save()
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
#                     # print(models.Wordform.objects.filter(pk=wordform.id).values())
#                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                                     object_id=wordform.id)
#                     dict_change.save()
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
#
#     # TODO Add form for commenting and duplicates resolution
#     # TODO Suggest translation constraint if marked in a csv
#
#
#
#     return added_translations