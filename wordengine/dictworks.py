from wordengine import models
from wordengine.global_const import *
from wordengine.uniworks import *
from collections import defaultdict
import csv
import codecs
from django.db import transaction, IntegrityError
import datetime
import re
import string


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


    # TODO: Modsave should record a DictChange, write to log and display action result

    return None


def check_cell_for_errors(csvcell, fields_to_check):
    error = ''
    errors = {}

    for field in fields_to_check:
        for char in SPECIAL_CHARS:
            if char in str(field):
                error += 'Unused special symbol: ' + char + ' in ' + str(field) + '\r\n'
        if re.search(RE_EXT_COMM, str(field)):
            error += 'Excessive extended comments marks in ' + str(field) + '\r\n'

    if error:
        errors[csvcell] = error

    return errors


def parse_csv_header(project):

    source_language = None
    lang_src_cols = []
    lang_trg_cols = []

    for colnum, value in enumerate(project.row[1:-1]):

        csvcell = models.CSVCell(row=0, col=colnum+1, value=value, project=project)
        csvcell.save()

        writing_system = None
        dialect = None
        processing = None

        col_split = value.strip().split('[', 1)
        if len(col_split) == 2:
            writing_system = col_split.pop().strip('] ')
        lang_dialect = col_split.pop().split('(', 1)
        if len(lang_dialect) == 2:
            dialect = lang_dialect.pop().strip(') ')
        language = lang_dialect.pop().strip()

        errors = check_cell_for_errors(csvcell, (language, dialect, writing_system, processing))

        column_literal = models.ProjectColumn(language_l=language, dialect_l=dialect, num=colnum+1,
                                              writing_system_l=writing_system,
                                              state='N', project=project, csvcell=csvcell)
        column_literal.save()

        # First column is treated as source language
        if not source_language:
            source_language = language

        if source_language == language:
            lang_src_cols.extend([(colnum+1, column_literal)])
        else:
            lang_trg_cols.extend([(colnum+1, column_literal)])

    return lang_src_cols, lang_trg_cols, errors


def get_ext_comments_from_csvcell(project):

    errors = {}
    ext_comments = []

    csvcell = models.CSVCell(row=project.rownum+1, col=len(project.row), value=project.row[-1], project=project)
    csvcell.save()
    ext_comm_split = RE_EXT_COMM.split(project.row[-1])
    if not ext_comm_split[0]:
        errors[project.row] += 'Something odd is in extended comment cell\r\n'

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

    csvcell = models.CSVCell(row=project.rownum, col=0, value=lexeme_literal, project=project)
    csvcell.save()

    lex_param = lexeme_literal.split('[', 1)
    synt_cat = lex_param.pop(0).strip()
    if len(lex_param) == 1:
        params = [s.strip('] ') for s in lex_param.pop(0).strip().split('[')]
    else:
        params = ''

    errors = check_cell_for_errors(csvcell, (params, synt_cat))

    lexeme_src = models.ProjectLexeme(syntactic_category=synt_cat, params=params, project=project, state='N',
                                      col=col, csvcell=csvcell)
    lexeme_src.save()

    return lexeme_src, errors


def get_wordforms_from_csvcell(project, lang_src_cols, lexeme_src, ext_comments):

    errors = {}
    first_col_wordforms = []

    for colnum, column_literal in lang_src_cols:
        lexeme_wordforms = project.row[colnum]
        if lexeme_wordforms:
            col_wordforms = []
            csvcell = models.CSVCell(row=project.rownum, col=colnum+1, value=lexeme_wordforms, project=project)
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

                    errors.update(check_cell_for_errors(csvcell, (spelling, comment, params)))

                    wordform = models.ProjectWordform(lexeme=lexeme_src, spelling=spelling, comment=comment,
                                                      params=params, project=project, state='N',
                                                      col=column_literal, csvcell=csvcell)
                    first_col_wordforms.extend(wordform)

                    wordform.save()
            else:
                for wf_num, current_wordform in enumerate(lexeme_wordforms.split('|')):
                    spelling = current_wordform
                    try:
                        original_wordform = first_col_wordforms[wf_num]
                    except IndexError:
                        errors[csvcell] += "Number of processed wordforms is more than the number of unprocessed\r\n"
                        continue

                    errors.update(check_cell_for_errors(csvcell, (spelling)))
                    proc_wordform = models.ProjectProcWordform(wordform=original_wordform, spelling=spelling,
                                                               col=column_literal)
                    col_wordforms.extend(proc_wordform)

                    proc_wordform.save()

                if len(col_wordforms) < len(first_col_wordforms):
                    errors[csvcell] += "Number of processed wordforms is less than the number of unprocessed\r\n"
        else:
            errors[project.row] = "Wordforms expected, but not found\r\n"

    return errors


def get_translations_from_csvcell(project, lang_trg_cols, lexeme_src, ext_comments):

    errors = {}
    for colnum, column_literal in lang_trg_cols:  # Iterate through multiple target languages
        lexeme_translations = project.row[colnum]
        if lexeme_translations:
            csvcell = models.CSVCell(row=project.rownum+1, col=colnum+2, value=lexeme_translations, project=project)
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

            errors.update(check_cell_for_errors(csvcell, (group_params, group_comment)))

            semantic_gr_src.save()

            for current_transl in lex_transl_split.pop().split('|'):
                cur_transl_split = current_transl.split('"', 1)  # ( [params] word [dialect] ), (comment")
                param_word_dialect = cur_transl_split.pop(0)
                params = []
                while param_word_dialect.strip()[0] == '[':
                    temp_split = param_word_dialect.split(']', 1)
                    params.append(temp_split.pop(0).strip('[ '))  # (param), ...
                    param_word_dialect = temp_split.pop(0)
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

                lexeme_trg = models.ProjectLexeme(syntactic_category=lexeme_src.syntactic_category, params=params,
                                                  project=project, state='N', col=column_literal, csvcell=csvcell)

                wordform = models.ProjectWordform(lexeme=lexeme_trg, spelling=spelling, project=project, state='N',
                                                  col=column_literal, csvcell=csvcell)

                semantic_gr_trg = models.ProjectSemanticGroup(dialect=transl_dialect, comment=transl_comment,
                                                              project=project, state='N', csvcell=csvcell)

                translation = models.ProjectTranslation(lexeme_1=lexeme_src, lexeme_2=lexeme_trg,
                                                        direction=1, semantic_group_1=semantic_gr_src,
                                                        semantic_group_2=semantic_gr_trg,
                                                        project=project, state='N')

                errors.update(check_cell_for_errors(csvcell, (params, spelling, transl_dialect, transl_comment)))

                lexeme_trg.save()
                wordform.save()
                semantic_gr_trg.save()
                translation.save()

    return errors


def parse_csv(request):
    """
    @param request:
    @return:

    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """

    # TODO Wrap with manual commit

    project = models.Project(user_uploader=request.user, timestamp_upload=datetime.datetime.now(),  # Always use UTC
                             filename=request.FILES['file'].name, source_id=request.POST['source'])
    project.errors = {}
    project.save()

    csvreader = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'), dialect=csv.excel_tab, delimiter='\t')
    # TODO If there are CSVCell objects of the project, do something with it

    for project.rownum, project.row in enumerate(csvreader):

        if project.rownum == 0:
            # Header must present, nothing to check
            lang_src_cols, lang_trg_cols, errors = parse_csv_header(project)
            project.errors.update(errors)
            continue

        if project.row[-1]:
            # Last column must be an extended comment column
            ext_comments = get_ext_comments_from_csvcell(project)
        else:
            ext_comments = []

        lexeme_literal = project.row[0]
        if lexeme_literal:  # Check if a new lexeme is in the row
            # Lexemes of a source language are bound to the first column with wordforms
            lexeme_src, errors = get_lexeme_from_csvcell(project, lexeme_literal, lang_src_cols[0][1])
            project.errors.update(errors)
        else:
            if not lexeme_src:
                project.errors[project.row] += 'No lexeme in the row\r\n'
                continue

        errors = get_wordforms_from_csvcell(project, lang_src_cols, lexeme_src, ext_comments)
        project.errors.update(errors)
        # TODO At least one wordform of a lexeme must present

        errors = get_translations_from_csvcell(project, lang_trg_cols, lexeme_src, ext_comments)
        project.errors.update(errors)
        # TODO Should I warn if no translations found?

    return project


def to_project_dict(project, model, field):
    src_obj = model.__name__
    fixed_keys = model.fixed_fks()
    fixed_keys.update(model.fixed_m2ms())
    if field in fixed_keys.values():
        term_type = fixed_keys[field].__name__
    else:
        term_type = None

    for value in model.objects.all().values(field).distinct():
        print(value)
        if value[field]:
            real_value = restore_list(value[field])
            for sg_value in real_value:
                pd = models.ProjectDictionary(value=sg_value, src_obj=src_obj, src_field=field, project=project,
                                              state='N', term_type=term_type)
                try:
                    pd.save()
                except IntegrityError:
                    pass  # TODO Should only occur if sg_value isn't unique. Reraise an error if that is not

    return None


def fill_project_dict(project):
    project_models = (models.ProjectLexeme, models.ProjectWordform, models.ProjectSemanticGroup)
    for model in project_models:
        for field in model.project_fields():
            to_project_dict(project, model, field)
    return None


def parse_upload(request):

    project, errors = parse_csv(request)
    fill_project_dict(project)

    return project.id, errors


def produce_project_model(project, model):
    created_objects = []

    for project_object in model.objects.filter(state='N').filter(project=project):

        transaction.set_autocommit(False)

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

        transaction.set_autocommit(True)

        created_objects.append(model_object)

    return created_objects


def produce_project(project):
    produce_project_model(project, models.ProjectLexeme)
    produce_project_model(project, models.ProjectWordform)
    produce_project_model(project, models.ProjectSemanticGroup)
    produce_project_model(project, models.ProjectTranslation)
    project.state = 'P'
    project.save()
    return None


# TODO Log every change - overload save() method? (Add dict_change)
#                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                                     object_id=wordform.id)
#                     dict_change.save()

    # dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
    #                                 object_id=translation.id)
    # dict_change.save()
