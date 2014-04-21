from wordengine import models
from collections import defaultdict
import csv
import io
import codecs
from django.db import transaction


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
            if row.get('Часть речи'):  # TODO Get default value from form

                lexeme_1 = models.Lexeme(language=language_1,
                                         syntactic_category=models.SyntacticCategory.objects.get(pk=1))  # TODO Get corresponding synt cat value
                print(dir(lexeme_1))
                lexeme_1.save()

                lexeme_2 = models.Lexeme(language=language_2,
                                         syntactic_category=models.SyntacticCategory.objects.get(pk=1))  # TODO Get corresponding synt cat value
                lexeme_2.save()

                translation = models.Translation(lexeme_1=lexeme_1, lexeme_2=lexeme_2)
                translation.save()
                translation.source.add(source_translation)

            try:
                # TODO Set default gr cat per every synt cat (get from order?)
                wordform_ortho_1 = models.Wordform(lexeme=lexeme_1, spelling=row.get('Написание 1'),
                                                   gramm_category_set=models.GrammCategorySet.objects.get(pk=1),
                                                   writing_system=writing_system_ortho_1)
            except KeyError:
                wordform_ortho_1 = None

            try:
                # TODO Set default gr cat per every synt cat (get from order?)
                wordform_phon_1 = models.Wordform(lexeme=lexeme_1, spelling=row.get('Произношение 1'),
                                                  gramm_category_set=models.GrammCategorySet.objects.get(pk=1),
                                                  writing_system=writing_system_phon_1)
            except KeyError:
                wordform_phon_1 = None

            try:
                # TODO Set default gr cat per every synt cat (get from order?)
                wordform_ortho_2 = models.Wordform(lexeme=lexeme_2, spelling=row.get('Написание 2'),
                                                   gramm_category_set=models.GrammCategorySet.objects.get(pk=1),
                                                   writing_system=writing_system_ortho_2)
            except KeyError:
                wordform_ortho_2 = None

            try:
                # TODO Set default gr cat per every synt cat (get from order?)
                wordform_phon_2 = models.Wordform(lexeme=lexeme_2, spelling=row.get('Произношение 2'),
                                                  gramm_category_set=models.GrammCategorySet.objects.get(pk=1),
                                                  writing_system=writing_system_phon_2)
            except KeyError:
                wordform_phon_2 = None

            wordform_ortho_1.save()
            wordform_phon_1.save()
            wordform_ortho_2.save()
            wordform_phon_2.save()

            try:
                wordform_ortho_1.dialect_multi.add(row.get('Диалект 1'))
            except ValueError:
                wordform_ortho_1.dialect_multi.add(dialect_1_default)
            wordform_ortho_1.source.add(source_1)

            try:
                wordform_phon_1.dialect_multi.add(row.get('Диалект 1'))
            except ValueError:
                wordform_phon_1.dialect_multi.add(dialect_1_default)
            wordform_phon_1.source.add(source_1)

            try:
                wordform_ortho_2.dialect_multi.add(row.get('Диалект 2'))
            except ValueError:
                wordform_ortho_2.dialect_multi.add(dialect_2_default)
            wordform_ortho_2.source.add(source_2)

            try:
                wordform_phon_2.dialect_multi.add(row.get('Диалект 2'))
            except ValueError:
                wordform_phon_2.dialect_multi.add(dialect_2_default)
            wordform_phon_2.source.add(source_2)
            # Does it need to be saved?

        transaction.rollback()
        transaction.set_autocommit(True)


            # TODO Add form for commenting and duplicates resolution
            # TODO Suggest translation constraint if marked in a csv