from wordengine import models
from wordengine.global_const import *
from wordengine.uniworks import *
from collections import defaultdict
import csv
import codecs
from django.db import transaction, IntegrityError
import datetime
import re

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
    # TODO Invalid search handling
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

    # TODO: Modsave should record a DictChange, write to log and display action result

    return None


def check_cell_for_errors(csvcell, fields, list_fields=[]):
    errors = []

    if list_fields:
        fields_to_check = fields + list_fields
    else:
        fields_to_check = fields

    for field in fields_to_check:
        for char in SPECIAL_CHARS:
            if char in str(field):
                errors.append((csvcell, 'Unused special symbol: ' + char + ' in ' + str(field)))
        if re.search(RE_EXT_COMM, str(field)):
            errors.append((csvcell, 'Excessive extended comments marks in ' + str(field)))

    return errors


def parse_csv_header(project):

    source_language = None
    lang_src_cols = []
    lang_trg_cols = []
    errors = []

    for colnum, value in enumerate(project.row[1:-1], 1):

        csvcell = models.CSVCell(row=0, col=colnum, value=value, project=project)
        csvcell.save()

        writing_system = ''
        dialect = ''

        col_split = value.strip().split('[', 1)
        if len(col_split) == 2:
            writing_system = col_split.pop().strip('] ')
        lang_dialect = col_split.pop().split('(', 1)
        if len(lang_dialect) == 2:
            dialect = lang_dialect.pop().strip(') ')
        language = lang_dialect.pop().strip()

        errors.extend(check_cell_for_errors(csvcell, (language, dialect, writing_system)))

        column_literal = models.ProjectColumn(language_l=language, dialect_l=dialect, num=colnum,
                                              writing_system_l=writing_system,
                                              state='N', project=project, csvcell=csvcell)
        column_literal.save()

        # First column is treated as source language
        if not source_language:
            source_language = language

        if source_language == language:
            lang_src_cols.append((colnum, column_literal))
        else:
            lang_trg_cols.append((colnum, column_literal))

    return lang_src_cols, lang_trg_cols, errors


def get_ext_comments_from_csvcell(project):

    errors = []
    ext_comments = []

    csvcell = models.CSVCell(row=project.rownum, col=len(project.row)-1, value=project.row[-1], project=project)
    csvcell.save()
    ext_comm_split = RE_EXT_COMM.split(project.row[-1])
    # if ext_comm_split[0]:
    #     errors.append((str(csvcell) + ' (ext comments)', 'Something odd is in extended comment cell'))
    # Temporary disabled (for testing purposes)

    odd = True
    temp_list = []
    for ec in ext_comm_split[1:]:
        if odd:
            temp_list = [ec]
            odd = not odd
        else:
            temp_list.append('"'+ec.strip()+'"')
            ext_comments.append(temp_list)
            odd = not odd

    return ext_comments, errors


def get_lexeme_from_csvcell(project, lexeme_literal, col):
    errors = []

    csvcell = models.CSVCell(row=project.rownum, col=0, value=lexeme_literal, project=project)
    csvcell.save()

    lex_param = lexeme_literal.split('[', 1)
    synt_cat = lex_param.pop(0).strip()
    if len(lex_param) == 1:
        params = [s.strip('] ') for s in lex_param.pop(0).strip().split('[')]
    else:
        params = ''

    errors.extend(check_cell_for_errors(csvcell, [synt_cat, ], params or []))

    lexeme_src = models.ProjectLexeme(syntactic_category=synt_cat, params=params, project=project, state='N',
                                      col=col, csvcell=csvcell)
    lexeme_src.save()

    return lexeme_src, errors


def get_wordforms_from_csvcell(project, lang_src_cols, lexeme_src, ext_comments, new_lexeme):

    errors = []
    first_col_wordforms = []

    for colnum, column_literal in lang_src_cols:
        lexeme_wordforms = project.row[colnum]

        if lexeme_wordforms:
            col_wordforms = []

            csvcell = models.CSVCell(row=project.rownum, col=colnum, value=lexeme_wordforms, project=project)
            csvcell.save()

            for ext_comment in ext_comments:
                if lexeme_wordforms.find(ext_comment[0]):
                    lexeme_wordforms = lexeme_wordforms.replace(ext_comment[0], ext_comment[1])

            if colnum == 1:
                for current_wordform in lexeme_wordforms.split('|'):
                    wordform_split = current_wordform.split('"', 1)  # ( spelling [params] ), (comment" )
                    spelling_params = wordform_split.pop(0).strip().split('[', 1)  # (spelling ), (params])
                    spelling = spelling_params.pop(0).strip()  # (spelling)
                    if len(spelling_params) == 1:
                        params = [s.strip('] ') for s in spelling_params.pop().strip().split('[')]  # (param), ...
                    else:
                        params = ''
                    if len(wordform_split) == 1:
                        comment = wordform_split.pop().strip('" ')  # (comment)
                    else:
                        comment = ''

                    errors.extend(check_cell_for_errors(csvcell, [spelling, comment], params or []))

                    wordform = models.ProjectWordform(lexeme=lexeme_src, comment=comment,
                                                      params=params, project=project, state='N',
                                                      col=column_literal, csvcell=csvcell)
                    wordform.save()
                    first_col_wordforms.append(wordform)
                    wordform_spell = models.ProjectProcWordform(wordform=wordform, spelling=spelling,
                                                                col=column_literal, csvcell=csvcell,
                                                                project=project, state='N')
            else:
                for wf_num, current_wordform in enumerate(lexeme_wordforms.split('|')):
                    spelling = current_wordform.strip()
                    try:
                        wordform = first_col_wordforms[wf_num]
                    except IndexError:
                        errors.append((csvcell, "Number of processed wordforms is more than the number of unprocessed"))
                        continue

                    errors.extend(check_cell_for_errors(csvcell, [spelling, ]))
                    proc_wordform = models.ProjectProcWordform(wordform=wordform, spelling=spelling,
                                                               col=column_literal, csvcell=csvcell,
                                                               project=project, state='N')
                    col_wordforms.append(proc_wordform)

                    proc_wordform.save()

                if len(col_wordforms) < len(first_col_wordforms):
                    errors.append((csvcell, "Number of processed wordforms is less than the number of unprocessed"))

        else:
            if new_lexeme:
                errors.append((str(project.row) + ' (source cols)', "Wordforms expected, but not found"))

    # TODO Add wordform deduplication
    # TODO Add param deduplication

    return errors


def get_translations_from_csvcell(project, lang_trg_cols, lexeme_src, ext_comments):

    errors = []
    translations_found = False

    for colnum, column_literal in lang_trg_cols:  # Iterate through multiple target languages
        lexeme_translations = project.row[colnum]
        if lexeme_translations:
            translations_found = True

            csvcell = models.CSVCell(row=project.rownum, col=colnum, value=lexeme_translations, project=project)
            csvcell.save()

            for ext_comment in ext_comments:
                if lexeme_translations.find(ext_comment[0]):
                    lexeme_translations = lexeme_translations.replace(ext_comment[0], ext_comment[1])

            lex_transl_split = lexeme_translations.split('@', 1)  # (group_params ), ( translations, ...)

            group_params = ''
            group_comment = ''
            if len(lex_transl_split) == 2:
                group_params_comment = lex_transl_split.pop(0).split('"', 1)  # ([params] ), (comment")
                if group_params_comment[0]:
                    group_params = [s.strip(' ]') for s in group_params_comment.pop(0).strip('[').split('[')]
                if len(group_params_comment) == 1:
                    group_comment = group_params_comment.pop().strip('" ')

            semantic_gr_src = models.ProjectSemanticGroup(params=group_params, comment=group_comment,
                                                          project=project, state='N', csvcell=csvcell)

            errors.extend(check_cell_for_errors(csvcell, [group_comment, ], group_params or []))

            semantic_gr_src.save()

            for current_transl in lex_transl_split.pop().split('|'):
                cur_transl_split = current_transl.split('"', 1)  # ( [params] word [dialect] ), (comment")
                param_word_dialect = cur_transl_split.pop(0)
                params = []
                while param_word_dialect.strip()[0] == '[':
                    temp_split = param_word_dialect.split(']', 1)
                    params.append(temp_split.pop(0).strip('[ '))  # (param), ...
                    param_word_dialect = temp_split.pop(0)
                params = params or ''
                word_dialect = param_word_dialect.strip().split('[', 1)  # (word ), (dialect])
                spelling = word_dialect.pop(0).strip()  # (word)
                if len(word_dialect) == 1:
                    transl_dialect = word_dialect.pop().strip(']')
                else:
                    transl_dialect = ''
                if len(cur_transl_split) == 1:
                    transl_comment = cur_transl_split.pop().strip('" ')  # (comment)
                else:
                    transl_comment = ''

                errors.extend(check_cell_for_errors(csvcell, [spelling, transl_dialect, transl_comment], params or []))

                lexeme_trg = models.ProjectLexeme(syntactic_category=lexeme_src.syntactic_category, params=params,
                                                  project=project, state='N', col=column_literal, csvcell=csvcell)

                lexeme_trg.save()

                wordform = models.ProjectWordform(lexeme=lexeme_trg, spelling=spelling, project=project, state='N',
                                                  col=column_literal, csvcell=csvcell)

                wordform.save()

                semantic_gr_trg = models.ProjectSemanticGroup(dialect=transl_dialect, comment=transl_comment,
                                                              project=project, state='N', csvcell=csvcell)

                semantic_gr_trg.save()

                translation = models.ProjectTranslation(lexeme_1=lexeme_src, lexeme_2=lexeme_trg,
                                                        direction=1, semantic_group_1=semantic_gr_src,
                                                        semantic_group_2=semantic_gr_trg,
                                                        project=project, state='N')

                translation.save()

    if not translations_found:
        errors.append((str(project.row) + ' (translations)', 'Translations expected, but not found'))

    # TODO Add wordform deduplication

    return errors


def parse_csv(request):
    """
    @param request:
    @return:

    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """

    project = models.Project(user_uploader=request.user, timestamp_upload=datetime.datetime.now(),  # Always use UTC
                             filename=request.FILES['file'].name, source_id=request.POST['source'])
    project.errors = []
    project.save()
    lang_src_cols = []
    lang_trg_cols = []

    csvreader = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'), dialect=csv.excel_tab, delimiter='\t')

    for project.rownum, project.row in enumerate(csvreader):

        if project.rownum == 0:
            # Header must present, nothing to check
            lang_src_cols, lang_trg_cols, errors = parse_csv_header(project)
            project.errors.extend(errors)
            continue

        if project.row[-1]:
            # Last column must be an extended comment column
            ext_comments, errors = get_ext_comments_from_csvcell(project)
            project.errors.extend(errors)
        else:
            ext_comments = []

        lexeme_literal = project.row[0]
        if lexeme_literal:  # Check if a new lexeme is in the row
            # Lexemes of a source language are bound to the first column with wordforms
            lexeme_src, errors = get_lexeme_from_csvcell(project, lexeme_literal, lang_src_cols[0][1])
            project.errors.extend(errors)
            new_lexeme = True
        else:
            if not lexeme_src:
                project.errors.append((str(project.row) + ' (lexemes)', 'No lexeme in the row'))
                continue
            else:
                new_lexeme = False

        errors = get_wordforms_from_csvcell(project, lang_src_cols, lexeme_src, ext_comments, new_lexeme)
        project.errors.extend(errors)

        errors = get_translations_from_csvcell(project, lang_trg_cols, lexeme_src, ext_comments)
        project.errors.extend(errors)

    return project


def fill_project_dict(project):
    project_models = (models.ProjectLexeme, models.ProjectWordform, models.ProjectSemanticGroup)
    for model in project_models:
        src_obj = model.__name__
        for field, term_type in model.project_fields().items():
            if type(term_type) == tuple:
                term_type = ''
            values = set()
            for value in model.objects.filter(project=project).values(field).distinct():
                if value[field]:
                    real_value = restore_list(value[field])
                    for sg_value in real_value:
                        values.add(sg_value)
            models.ProjectDictionary.objects.bulk_create([models.ProjectDictionary(value=val, src_obj=src_obj,
                                                                                   project=project, state='N',
                                                                                   term_type=term_type)
                                                          for val in values])
    return None


def parse_upload(request):

    transaction.set_autocommit(False)
    project = parse_csv(request)
    fill_project_dict(project)
    if project.errors:
        transaction.rollback()
    transaction.set_autocommit(True)

    return project.id, project.errors


def produce_project_model(project, model):
    created_objects = []

    for project_object in model.objects.filter(state='N', project=project):

        fields = project_object.fields()
        model_object = model.real_model()(**fields)
        model_object.save()
        project_object.result = model_object

        m2m_fields = project_object.m2m_fields()
        for m2m_field in m2m_fields:
            getattr(model_object, m2m_field).add(*m2m_fields[m2m_field])

        m2m_thru_fields = project_object.m2m_thru_fields()
        for m2m_thru_field in m2m_thru_fields:
            fields = m2m_thru_fields[m2m_thru_field]
            m2m_thru = m2m_thru_field(**fields)
            m2m_thru.save()

        project_object.state = 'P'
        project_object.save()

        created_objects.append(model_object)

    return created_objects


def produce_project(project):
    transaction.set_autocommit(False)
    # TODO Check if syntactic categories present in language
    produce_project_model(project, models.ProjectLexeme)
    produce_project_model(project, models.ProjectWordform)
    produce_project_model(project, models.ProjectProcWordform)
    produce_project_model(project, models.ProjectSemanticGroup)
    produce_project_model(project, models.ProjectTranslation)
    project.state = 'P'
    project.save()
    transaction.set_autocommit(True)
    return None


# TODO Log every change - overload save() method? (Add dict_change)
#                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                                     object_id=wordform.id)
#                     dict_change.save()

    # dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
    #                                 object_id=translation.id)
    # dict_change.save()
