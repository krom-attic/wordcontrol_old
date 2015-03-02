import codecs
import csv

from wordengine import models
from wordengine.global_const import *


class CSVRow():
    def __init__(self, project, num, data):
        self.project = project
        self.num = num
        self.data = data
        self.errors = []

    def parse_csv_header(self):

        source_language = None
        lang_src_cols = []
        lang_trg_cols = []
        errors = []

        for colnum, value in enumerate(self.data[1:-1], 1):

            csvcell = models.CSVCell(rownum=0, colnum=colnum, value=value, project=self.project)
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

            errors.extend(csvcell.check_for_errors((language, dialect, writing_system)))
            # TODO Check check_for_errors usage

            column_literal = models.ProjectColumn(language_l=language, dialect_l=dialect, num=colnum,
                                                  writing_system_l=writing_system,
                                                  state='N', project=self.project, csvcell=csvcell)
            column_literal.save()

            # First column is treated as source language
            if not source_language:
                source_language = language

            if source_language == language:
                lang_src_cols.append((colnum, column_literal))
            else:
                lang_trg_cols.append((colnum, column_literal))

        return lang_src_cols, lang_trg_cols, errors

    def get_ext_comments(self):

        errors = []
        ext_comments = {}

        csvcell = models.CSVCell(rownum=self.num, colnum=self.project.colsnum-1, value=self.data[-1],
                                 project=self.project)
        csvcell.save()

        ext_comm_split = RE_EXT_COMM.split(self.data[-1])
        if ext_comm_split[0]:
            errors.append((str(csvcell), 'CSV-10', '(ext comments)'))

        for i in range(1, len(ext_comm_split), 2):
            ext_comments[ext_comm_split[i]] = '"'+ext_comm_split[i+1].strip()+'"'
            # Out of range seems to be impossible

        return ext_comments, errors

    def get_lexeme(self):
        csvcell = models.CSVCell(rownum=self.num, colnum=0, value=self.data[0], project=self.project)
        csvcell.save()

        split_str, errors = csvcell.split_data(self.data[0], False, True, False)
        synt_cat, params = split_str
        # Lexemes of a source language are bound to the first column with wordforms
        lexeme_src = models.ProjectLexeme(syntactic_category=synt_cat, params=params, project=self.project, state='N',
                                          col=self.project.lang_src_cols[0][1], csvcell=csvcell)
        lexeme_src.save()

        return lexeme_src, errors


def get_wordforms_from_csvcell(project, lang_src_cols, lexeme_src, ext_comments, new_lexeme):

    errors = []
    first_col_wordforms = []

    for colnum, column_literal in lang_src_cols:
        lexeme_wordforms = project.row[colnum]

        if lexeme_wordforms:

            csvcell = models.CSVCell(row=project.rownum, col=colnum, value=lexeme_wordforms, project=project)
            csvcell.save()

            for ext_comment_marker, ext_comment in ext_comments.items():
                if lexeme_wordforms.find(ext_comment_marker):
                    lexeme_wordforms = lexeme_wordforms.replace(ext_comment_marker, ext_comment)

            if colnum == 1:
                for current_wordform in lexeme_wordforms.split('|'):
                    wordform_split = current_wordform.split('"', 1)  # ( spelling [params] ), (comment" )
                    spelling_params = wordform_split.pop(0).strip().split('[', 1)  # (spelling ), (params])
                    spelling = spelling_params.pop(0).strip()  # (spelling)
                    if len(spelling_params) == 1:
                        params = tuple(s.strip('] ') for s in spelling_params.pop().strip().split('['))  # (param), ...
                    else:
                        params = ''
                    if len(wordform_split) == 1:
                        comment = wordform_split.pop().strip('" ')  # (comment)
                    else:
                        comment = ''

                    errors.extend(check_cell_for_errors(csvcell, (spelling, comment), params or ()))

                    wordform = models.ProjectWordform(lexeme=lexeme_src, comment=comment,
                                                      params=params, project=project, state='N',
                                                      col=column_literal, csvcell=csvcell)
                    wordform.save()
                    first_col_wordforms.append(wordform)

                    wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                                 col=column_literal, csvcell=csvcell,
                                                                 project=project, state='N', is_processed=False)
                    wordform_spell.save()
            else:
                wf_num = -1
                for wf_num, current_wordform in enumerate(lexeme_wordforms.split('|')):
                    spelling = current_wordform.strip()
                    try:
                        wordform = first_col_wordforms[wf_num]
                    except IndexError:
                        errors.append((csvcell, "Number of processed wordforms is more than the number of unprocessed"))
                        continue

                    errors.extend(check_cell_for_errors(csvcell, [spelling, ]))
                    wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                                 col=column_literal, csvcell=csvcell,
                                                                 project=project, state='N', is_processed=True)
                    wordform_spell.save()

                if wf_num + 1 < len(first_col_wordforms):
                    errors.append((csvcell, "Number of processed wordforms is less than the number of unprocessed"))

        else:
            if new_lexeme:
                errors.append((str(project.row) + ' (source cols)', "Wordforms expected, but not found"))

    # TODO Add wordform deduplication
    # TODO Add param deduplication

    return errors


# def split_translation_group(str_to_split):
#     group_params_comment = str_to_split.split('"', 1)  # ([params] ), (comment")
#     if group_params_comment[0]:
#         group_params = tuple(s.strip(' ]') for s in group_params_comment.pop(0).strip('[').split('['))
#     else:
#         group_params = ()
#     if len(group_params_comment) == 1:
#         group_comment = group_params_comment.pop().strip('" ')
#     else:
#         group_comment = ''
#     return group_params, group_comment


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

            if len(lex_transl_split) == 2:
                group_params, group_comment = split_translation_group(lex_transl_split.pop(0))
            else:
                group_params = ()
                group_comment = ''

            # TODO Numbering of Lexemes and SemanticCategories in Translations are swapped
            semantic_gr_src = models.ProjectSemanticGroup(params=group_params, comment=group_comment,
                                                          project=project, state='N', csvcell=csvcell)

            errors.extend(check_cell_for_errors(csvcell, (group_comment, ), group_params or ()))

            semantic_gr_src.save()

            for current_transl in lex_transl_split.pop().split('|'):
                cur_transl_split = current_transl.split('"', 1)  # ( [params] word [dialect] ), (comment")
                param_word_dialect = cur_transl_split.pop(0)
                params = []
                while param_word_dialect.strip()[0] == '[':
                    temp_split = param_word_dialect.split(']', 1)
                    params.append(temp_split.pop(0).strip('[ '))  # (param), ...
                    param_word_dialect = temp_split.pop(0)
                params = tuple(params) or ''
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

                errors.extend(check_cell_for_errors(csvcell, (spelling, transl_dialect, transl_comment), params or ()))

                lexeme_trg = models.ProjectLexeme(syntactic_category=lexeme_src.syntactic_category, params=params,
                                                  project=project, state='N', col=column_literal, csvcell=csvcell)

                lexeme_trg.save()

                wordform = models.ProjectWordform(lexeme=lexeme_trg, project=project, state='N',
                                                  col=column_literal, csvcell=csvcell)

                wordform.save()

                wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling, project=project,
                                                             state='N', col=column_literal, csvcell=csvcell,
                                                             is_processed=False)

                wordform_spell.save()

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


# # TODO Create check_row to check that *Ns are correct
#         '''
#         if char == '*':
#             ext_comm_met = True
#             continue
#         elif ext_comm_met:
#             if char not in string.digits:
#                 ext_comm_met = False
#             continue
#         '''


def parse_csv(csvreader, project):

    project.errors = []
    # Errors storage format: whole data, error code, erroneous fragment (optional)
    project.save()  # Required

    for num, data in enumerate(csvreader):
        row = CSVRow(project, num, data)
        if row.num == 0:
            # Header must present, nothing to check
            project.lang_src_cols, project.lang_trg_cols, project.errors = row.parse_csv_header()
            project.colsnum = len(row.data)
            continue

        else:
            if row.data[-1]:
                # Last column must be an extended comment column
                ext_comments, errors = row.get_ext_comments()
                project.errors.extend(errors)
            else:
                ext_comments = {}
            # TODO? Alter row data with ext_comments?
            if row.data[0]:  # Check if a new lexeme is in the row
                lexeme_src, errors = row.get_lexeme()
                project.errors.extend(errors)
                new_lexeme = True
            else:
                if not lexeme_src:
                    project.errors.append((str(row.data) + ' (lexemes)', 'CSV-9'))
                    continue
                else:
                    new_lexeme = False

            errors = get_wordforms_from_csvcell(row, lang_src_cols, lexeme_src, ext_comments, new_lexeme)
            project.errors.extend(errors)

            errors = get_translations_from_csvcell(row, lang_trg_cols, lexeme_src, ext_comments)
            project.errors.extend(errors)

    return project


def get_csv(csvfile):
    """
    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """
    return csv.reader(codecs.iterdecode(csvfile, 'utf-8'), dialect=csv.excel_tab, delimiter='\t')