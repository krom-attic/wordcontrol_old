from wordengine import models
from collections import defaultdict
import csv
import io
import codecs
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist


# Common functions here

def find_lexeme_wordforms(word_search, exact):

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


# def add_new_word():
#     transaction.set_autocommit(False)
#     try:
#         if lexeme_validated == 2:
#             lexeme = lexeme_form.save()
#         wordform_form_initial = models.Wordform(lexeme=lexeme)
#         self.wordform_form = self.wordform_form_class(request.POST, instance=wordform_form_initial)
#         if self.wordform_form.is_valid():
#             wordform = self.wordform_form.save()
#             dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                             object_id=wordform.id)
#             dict_change.save()
#             messages.success(request, "The word has been added")
#             is_saved = True
#     finally:
#         if not is_saved:
#             transaction.rollback()
#         transaction.set_autocommit(True)


def parse_data_import(postdata, datafile):  # TODO Fix field name hardcode

    content = datafile.read()
    encoding = 'utf-16'    # TODO http://pypi.python.org/pypi/chardet
    # csv_dialect = csv.Sniffer().sniff(content)  # TODO CSV Detect dialect
    content = str(content.decode(encoding, 'replace'))  # Why 'replace'?
    filestream = io.StringIO(content)

    with filestream as csvfile:  # TODO Wrap with manual commit
        reader = csv.DictReader(csvfile, delimiter=',')  # quoting=csv.QUOTE_NONE?
        language_1 = models.Language.objects.get(pk=postdata['language_1'])
        language_2 = models.Language.objects.get(pk=postdata['language_2'])
        source_translation = models.Source.objects.get(pk=postdata['source_translation'])
        WORD_SOURCES = {0: None, 1: source_translation}
        source_1 = WORD_SOURCES.get(postdata['source_1'])
        source_2 = WORD_SOURCES.get(postdata['source_2'])
        writing_system_ortho_1 = models.WritingSystem.objects.get(pk=postdata['writing_system_ortho_1'])
        writing_system_phon_1 = models.WritingSystem.objects.get(pk=postdata['writing_system_phon_1'])
        writing_system_ortho_2 = models.WritingSystem.objects.get(pk=postdata['writing_system_ortho_2'])
        writing_system_phon_2 = models.WritingSystem.objects.get(pk=postdata['writing_system_phon_2'])
        dialect_1_default = models.Dialect.objects.get(pk=postdata['dialect_1_default'])
        dialect_2_default = models.Dialect.objects.get(pk=postdata['dialect_2_default'])

        transaction.set_autocommit(False)
        for row in reader:  # Split larger files by chunks?
            if row.get('Часть речи'):
                synt_cat = models.SyntacticCategory.objects.get(term_abbr=row.get('Часть речи'))

                lexeme_1 = models.Lexeme(language=language_1, syntactic_category=synt_cat)
                lexeme_1.save()
                print(models.Lexeme.objects.filter(pk=lexeme_1.id).values())

                try:
                    main_gr_cat_1 = models.GrammCategorySet.objects.filter(language=language_1,
                                                                           syntactic_category=synt_cat)\
                        .order_by('position').first()
                except ObjectDoesNotExist:
                    main_gr_cat_1 = None

                print(main_gr_cat_1)

                lexeme_2 = models.Lexeme(language=language_2, syntactic_category=synt_cat)
                lexeme_2.save()
                print(models.Lexeme.objects.filter(pk=lexeme_2.id).values())

                try:
                    main_gr_cat_2 = models.GrammCategorySet.objects.filter(language=language_2,
                                                                           syntactic_category=synt_cat)\
                        .order_by('position').first()

                except ObjectDoesNotExist:
                    main_gr_cat_2 = None

                print(main_gr_cat_2)

                translation = models.Translation(lexeme_1=lexeme_1, lexeme_2=lexeme_2)
                translation.save()
                translation.source.add(source_translation)
                print(models.Translation.objects.filter(pk=translation.id).values())

            WORDFORM_PARAMS = (
                (lexeme_1, main_gr_cat_1, 'Диалект 1', dialect_1_default, source_1),
                (lexeme_2, main_gr_cat_2, 'Диалект 2', dialect_2_default, source_2),
            )

            ROW_GET_PARAMS = (
                ('Написание 1', writing_system_ortho_1, WORDFORM_PARAMS[0]),
                ('Произношение 1', writing_system_phon_1, WORDFORM_PARAMS[0]),
                ('Написание 2', writing_system_ortho_2, WORDFORM_PARAMS[1]),
                ('Произношение 2', writing_system_phon_2, WORDFORM_PARAMS[1]),
            )

            for current_row_params in ROW_GET_PARAMS:
                current_word = row.get(current_row_params[0])
                if current_word:
                    wordform = models.Wordform(lexeme=current_row_params[2][0], spelling=current_word,
                                                       gramm_category_set=current_row_params[2][1],
                                                       writing_system=current_row_params[1])
                    wordform.save()
                    try:
                        wordform.dialect_multi.add(current_row_params[2][2])
                    except ValueError:
                        wordform.dialect_multi.add(current_row_params[2][3])
                    try:
                        wordform.source.add(current_row_params[2][4])
                    except IntegrityError:
                        pass
                    print(models.Wordform.objects.filter(pk=wordform.id).values())

            # Does it need to be saved after "add"?

        transaction.rollback()
        transaction.set_autocommit(True)


            # TODO Add form for commenting and duplicates resolution
            # TODO Suggest translation constraint if marked in a csv