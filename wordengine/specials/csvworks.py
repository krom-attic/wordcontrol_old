import codecs
import csv

from wordengine import models
from wordengine.global_const import *


class CSVCell(models.ProjectCSVCell):
    class Meta:
        proxy = True

    def split_header(self, str_to_split):
        errors = []

        writing_system = ''
        dialect = ''

        col_split = str_to_split.strip().split('[', 1)
        if len(col_split) == 2:
            writing_system = col_split.pop().strip('] ')
        lang_dialect = col_split.pop().split('(', 1)
        if len(lang_dialect) == 2:
            dialect = lang_dialect.pop().strip(') ')
        language = lang_dialect.pop().strip()

        errors += [(self, CSVError(e[0], e[1])) for e in self.check_for_errors(language) +
                   self.check_for_errors(dialect) + self.check_for_errors(writing_system)]

        return language, dialect, writing_system, errors

    @staticmethod
    def check_for_errors(checked_value):
        """

        :param checked_value:
        :return: [(error_code, error_details), ...]
        """
        unexpected_chars = [('CSV-7', char + ' in "' + checked_value + '"') for char in checked_value
                            if char in SPECIAL_CHARS]
        ext_comment_marks = RE_EXT_COMM.findall(checked_value)
        if ext_comment_marks:
            unexpected_ext_comments = [('CSV-8', mark + ' in "' + checked_value + '"')
                                       for mark in ext_comment_marks]
            return unexpected_chars + unexpected_ext_comments
        else:
            return unexpected_chars

    def split_data(self, str_to_split, has_pre_params, has_data, has_comment):
        """
        Splits str_to_split against pattern:
            [pre_params] data [post_params] "comment"
        Post params may present in any case
        :param str_to_split: Original string
        :param has_pre_params: Pre params MAY present
        :param has_data: Indicates whether data MUST present or MUST be empty
        :param has_comment: Comment MAY present
        :return: list of list for each part that may or must present
        """

        errors = []
        data = ''
        pre_params = []
        post_params = []
        comment = ''

        split_str = RE_PARAM.split(str_to_split)
        for i in range(len(split_str)-1):
            if i % 2 == 0:
                if split_str[i].strip():
                    if data:
                        # data already found
                        errors.append((self, CSVError('CSV-3', split_str[i].strip())))
                    else:
                        data = split_str[i].strip()
            else:
                param = split_str[i][1:-1]
                errors += [(self, CSVError(e[0], e[1])) for e in self.check_for_errors(param)]
                if data or not has_data:
                    post_params.append(param)
                else:
                    pre_params.append(param)

        last_split = RE_COMMENT.split(split_str[-1].strip(), 1)
        if last_split[0].strip():
            if data:
                # data already found
                errors.append((self, CSVError('CSV-4', last_split[0].strip())))
            else:
                data = last_split[0].strip()

        if len(last_split) > 1:
            comment = last_split[1][1:-1]
            if last_split[2] or len(last_split) > 3:
                errors.append((self, CSVError('CSV-5', last_split[2:])))

        result = []

        if has_pre_params:
            result.append(pre_params or '')
        else:
            if pre_params:
                errors.append((self, CSVError('CSV-1', str(pre_params))))

        if has_data:
            errors += [(self, CSVError(e[0], e[1])) for e in self.check_for_errors(data)]
            result.append(data)
            if not data:
                errors.append((self, CSVError('CSV-2')))
        else:
            if data:
                errors.append((self, CSVError('CSV-3', data)))

        result.append(post_params or '')

        if has_comment:
            errors += [(self, e[0], e[1]) for e in self.check_for_errors(comment)]
            result.append(comment)
        else:
            if comment:
                errors.append((self, CSVError('CSV-6', comment)))

        result.append(errors)

        return result


class CSVRow():
    last_lexeme_src = None

    def __init__(self, project, num, data):
        self.project = project
        self.num = num
        self.data = data
        self.ext_comments = {}

    def set_last_lexeme(self, new_lexeme):
        self.__class__.last_lexeme_src = new_lexeme

    def parse_csv_header(self):

        source_language = None
        lang_src_cols = []
        lang_trg_cols = []
        errors = []

        for colnum, value in enumerate(self.data[1:-1], 1):

            csvcell = CSVCell(rownum=self.num, colnum=colnum, value=value, project=self.project)
            csvcell.save()

            language, dialect, writing_system, split_errors = csvcell.split_header(value)
            errors += split_errors

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

        # Last column must be an extended comment column
        if self.data[-1]:
            csvcell = CSVCell(rownum=self.num, colnum=self.project.colsnum-1, value=self.data[-1], project=self.project)
            csvcell.save()

            ext_comm_split = RE_EXT_COMM.split(self.data[-1])
            if ext_comm_split[0]:
                errors.append((str(csvcell), CSVError('CSV-10', ext_comm_split[0])))

            for i in range(1, len(ext_comm_split), 2):
                self.ext_comments[ext_comm_split[i]] = '"'+ext_comm_split[i+1].strip()+'"'
                # Out of range seems to be impossible

        return errors

    def produce_lexeme(self):

        errors = []

        if self.data[0]:  # Check if a new lexeme is in the row

            csvcell = CSVCell(rownum=self.num, colnum=0, value=self.data[0], project=self.project)
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

    def save_fst_wordforms(self, csvcell, current_wordform, column_literal):

        spelling, params, comment, errors = csvcell.split_data(current_wordform, False, True, True)

        wordform = models.ProjectWordform(lexeme=self.last_lexeme_src, comment=comment,
                                          params=params, project=self.project, state='N',
                                          col=column_literal, csvcell=csvcell)
        wordform.save()

        wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                     col=column_literal, csvcell=csvcell,
                                                     project=self.project, state='N',
                                                     is_processed=False)
        wordform_spell.save()

        return wordform, errors

    def save_other_wordforms(self, csvcell, current_wordform, column_literal, first_col_wordforms, wf_num):
        errors = []

        spelling = current_wordform.strip()

        # This may cause IndexError
        wordform = first_col_wordforms[wf_num]

        errors += [(self, CSVError(e[0], e[1])) for e in csvcell.check_for_errors(spelling)]

        wordform_spell = models.ProjectWordformSpell(wordform=wordform, spelling=spelling,
                                                     col=column_literal, csvcell=csvcell,
                                                     project=self.project, state='N', is_processed=True)
        wordform_spell.save()

        return errors

    def produce_wordforms(self):

        errors = []
        first_col_wordforms = []

        for colnum, column_literal in self.project.lang_src_cols:
            lexeme_wordforms = self.data[colnum]

            if not lexeme_wordforms:
                if self.data[0]:
                    errors.append(('Row {} (source cols)'.format(self.num), CSVError('CSV-11')))
                continue

            csvcell = CSVCell(rownum=self.num, colnum=colnum, value=lexeme_wordforms, project=self.project)
            csvcell.save()

            lexeme_wordforms = self.use_ext_comments(lexeme_wordforms)

            if colnum == 1:
                for current_wordform in lexeme_wordforms.split('|'):
                    wordform, split_errors = self.save_fst_wordforms(csvcell, current_wordform, column_literal)
                    errors += split_errors
                    first_col_wordforms.append(wordform)
            else:
                wf_num = -1
                for wf_num, current_wordform in enumerate(lexeme_wordforms.split('|')):
                    try:
                        errors += self.save_other_wordforms(csvcell, current_wordform, column_literal,
                                                            first_col_wordforms, wf_num)
                    except IndexError:
                        errors.append((csvcell, CSVError('CSV-12')))
                        continue

                if wf_num + 1 < len(first_col_wordforms):
                    errors.append((csvcell, CSVError('CSV-13')))

        # TODO Add param deduplication ????

        return errors

    def save_translations(self, csvcell, current_transl, column_literal, semantic_gr_src):

        params, spelling, transl_dialect, transl_comment, errors = csvcell.split_data(current_transl, True, True, True)

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

        return errors

    def produce_translations(self):

        errors = []
        translations_found = False

        for colnum, column_literal in self.project.lang_trg_cols:  # Iterate through multiple target languages
            lexeme_translations = self.data[colnum]
            if not lexeme_translations:
                continue

            translations_found = True

            csvcell = CSVCell(rownum=self.num, colnum=colnum, value=lexeme_translations, project=self.project)
            csvcell.save()

            lexeme_translations = self.use_ext_comments(lexeme_translations)
            lex_transl_split = lexeme_translations.split('@', 1)  # (group_params ), ( translations, ...)

            if len(lex_transl_split) == 2:
                group_params, group_comment, split_errors = csvcell.split_data(lex_transl_split[0], False, False,
                                                                               True)
                errors += split_errors
            else:
                group_params, group_comment = '', ''

            semantic_gr_src = models.ProjectSemanticGroup(params=group_params, comment=group_comment,
                                                          project=self.project, state='N', csvcell=csvcell)

            semantic_gr_src.save()

            for current_transl in lex_transl_split.pop().split('|'):
                errors += self.save_translations(csvcell, current_transl, column_literal, semantic_gr_src)

        if not translations_found:
            errors.append(('Row {} (translations)'.format(self.num), CSVError('CSV-14')))

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

            project.errors += row.get_ext_comments()

            project.errors += row.produce_lexeme()

            if not row.last_lexeme_src:
                project.errors.append(('Row ' + str(row.num+1) + ' (lexemes)', CSVError('CSV-9')))
                continue

            project.errors += row.produce_wordforms()

            project.errors += row.produce_translations()

    return project


def get_csv(csvfile):
    """
    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """
    return csv.reader(codecs.iterdecode(csvfile, 'utf-8'), dialect=csv.excel_tab, delimiter='\t')
