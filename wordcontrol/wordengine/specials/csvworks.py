import codecs
import csv

from wordengine import models
from wordengine.global_const import *


class CSVRow():
    last_lexeme_src = None

    def __init__(self, project, num, data):
        self.project = project
        self.num = num
        self.data = data
        self.errors = []
        self.ext_comments = {}

    def set_last_lexeme(self, new_lexeme):
        self.__class__.last_lexeme_src = new_lexeme

    def parse_csv_header(self):

        source_language = None
        lang_src_cols = []
        lang_trg_cols = []
        errors = []

        for colnum, value in enumerate(self.data[1:-1], 1):

            csvcell = models.CSVCell(rownum=self.num, colnum=colnum, value=value, project=self.project)
            csvcell.save()

            language, dialect, writing_system, errors = csvcell.split_header(value)

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
        self.ext_comments = {}

        # Last column must be an extended comment column
        if self.data[-1]:
            csvcell = models.CSVCell(rownum=self.num, colnum=self.project.colsnum-1, value=self.data[-1],
                                     project=self.project)
            csvcell.save()

            ext_comm_split = RE_EXT_COMM.split(self.data[-1])
            if ext_comm_split[0]:
                errors.append((str(csvcell), WCError('CSV-10', ext_comm_split[0])))

            for i in range(1, len(ext_comm_split), 2):
                self.ext_comments[ext_comm_split[i]] = '"'+ext_comm_split[i+1].strip()+'"'
                # Out of range seems to be impossible

        return errors

    def produce_lexeme(self):

        errors = []

        if self.data[0]:  # Check if a new lexeme is in the row

            csvcell = models.CSVCell(rownum=self.num, colnum=0, value=self.data[0], project=self.project)
            csvcell.save()

            synt_cat, params, errors = csvcell.split_data(self.data[0], False, True, False)
            # Lexemes of a source language are bound to the first column with wordforms
            lexeme_src = models.ProjectLexeme(syntactic_category=synt_cat, params=params, project=self.project,
                                              state='N', col=self.project.lang_src_cols[0][1], csvcell=csvcell)
            lexeme_src.save()

            self.set_last_lexeme(lexeme_src)

        return errors

    def use_ext_comments(self, text):
        for ext_comment_marker in list(self.ext_comments):
            if text.find(ext_comment_marker) > -1:
                ext_comment = self.ext_comments.pop(ext_comment_marker)
                text = text.replace(ext_comment_marker, ext_comment, 1)
        return text

    def produce_wordforms(self):

        errors = []
        first_col_wordforms = []

        for colnum, column_literal in self.project.lang_src_cols:
            lexeme_wordforms = self.data[colnum]

            if lexeme_wordforms:

                csvcell = models.CSVCell(rownum=self.num, colnum=colnum, value=lexeme_wordforms, project=self.project)
                csvcell.save()

                lexeme_wordforms = self.use_ext_comments(lexeme_wordforms)

                if colnum == 1:
                    for current_wordform in lexeme_wordforms.split('|'):
                        spelling, params, comment, errors = csvcell.split_data(current_wordform, False, True, True)

                        wordform = models.ProjectWordform(lexeme=self.last_lexeme_src, comment=comment,
                                                          params=params, project=self.project, state='N',
                                                          col=column_literal, csvcell=csvcell)
                        wordform.save()
                        first_col_wordforms.append(wordform)

                        wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                                     col=column_literal, csvcell=csvcell,
                                                                     project=self.project, state='N',
                                                                     is_processed=False)
                        wordform_spell.save()
                else:
                    wf_num = -1
                    for wf_num, current_wordform in enumerate(lexeme_wordforms.split('|')):
                        spelling = current_wordform.strip()
                        try:
                            wordform = first_col_wordforms[wf_num]
                        except IndexError:
                            errors.append((csvcell, WCError('CSV-12')))
                            continue

                        errors.extend(csvcell.check_for_errors(spelling))

                        wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                                     col=column_literal, csvcell=csvcell,
                                                                     project=self.project, state='N', is_processed=True)
                        wordform_spell.save()

                    if wf_num + 1 < len(first_col_wordforms):
                        errors.append((csvcell, WCError('CSV-13')))

            else:
                if self.data[0]:
                    errors.append(('Row ' + str(self.num) + ' (source cols)', WCError('CSV-11')))

        # TODO Add param deduplication ????

        return errors

    def produce_translations(self):

        errors = []
        translations_found = False

        for colnum, column_literal in self.project.lang_trg_cols:  # Iterate through multiple target languages
            lexeme_translations = self.data[colnum]
            if lexeme_translations:
                translations_found = True

                csvcell = models.CSVCell(rownum=self.num, colnum=colnum, value=lexeme_translations,
                                         project=self.project)
                csvcell.save()

                lexeme_translations = self.use_ext_comments(lexeme_translations)

                lex_transl_split = lexeme_translations.split('@', 1)  # (group_params ), ( translations, ...)

                if len(lex_transl_split) == 2:
                    group_params, group_comment, errors = csvcell.split_data(lex_transl_split[0], False, False, True)
                else:
                    group_params = ''
                    group_comment = ''

                semantic_gr_src = models.ProjectSemanticGroup(params=group_params, comment=group_comment,
                                                              project=self.project, state='N', csvcell=csvcell)

                semantic_gr_src.save()

                for current_transl in lex_transl_split.pop().split('|'):
                    params, spelling, transl_dialect, transl_comment, errors =\
                        csvcell.split_data(current_transl, True, True, True)

                    lexeme_trg = models.ProjectLexeme(syntactic_category=self.last_lexeme_src.syntactic_category,
                                                      params=params, project=self.project, state='N',
                                                      col=column_literal, csvcell=csvcell)

                    lexeme_trg.save()

                    wordform = models.ProjectWordform(lexeme=lexeme_trg, project=self.project, state='N',
                                                      col=column_literal, csvcell=csvcell)

                    wordform.save()

                    wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                                 project=self.project, state='N', col=column_literal,
                                                                 csvcell=csvcell, is_processed=False)

                    wordform_spell.save()

                    semantic_gr_trg = models.ProjectSemanticGroup(dialect=transl_dialect, comment=transl_comment,
                                                                  project=self.project, state='N', csvcell=csvcell)

                    semantic_gr_trg.save()

                # TODO Numbering of Lexemes and SemanticCategories in Translations are swapped - proof
                    translation = models.ProjectTranslation(lexeme_1=self.last_lexeme_src, lexeme_2=lexeme_trg,
                                                            direction=1, semantic_group_1=semantic_gr_src,
                                                            semantic_group_2=semantic_gr_trg,
                                                            project=self.project, state='N')

                    translation.save()

        if not translations_found:
            errors.append(('Row ' + str(self.num) + ' (translations)', WCError('CSV-14')))

        # TODO Add wordform deduplication ????

        return errors


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

            project.errors.extend(row.get_ext_comments())

            project.errors.extend(row.produce_lexeme())

            if not row.last_lexeme_src:
                project.errors.append(('Row ' + str(row.num+1) + ' (lexemes)', WCError('CSV-9')))
                continue

            project.errors.extend(row.produce_wordforms())

            project.errors.extend(row.produce_translations())

    return project


def get_csv(csvfile):
    """
    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """
    return csv.reader(codecs.iterdecode(csvfile, 'utf-8'), dialect=csv.excel_tab, delimiter='\t')
