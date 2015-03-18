from wordengine.commonworks import *
from wordengine import models
from wordengine.specials import csvworks

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import datetime


class ProjectError(Exception):
    """
    Errors in imported CSV files
    """
    pass


class ProjectFromCSV(models.Project):

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ProjectFromCSV, self).__init__(*args, **kwargs)
        if request:
            self.user_uploader = request.user
            self.timestamp_upload = datetime.datetime.now()
            self.filename = request.FILES['file'].name
            self.source_id = request.POST['source']
            self.csv_reader = csvworks.get_csv(request.FILES['file'])

    def prepare(self):
        # Errors storage format: whole data, error code, erroneous fragment (optional)
        self.errors = []
        try:
            with transaction.atomic():
                self.save()  # Required
                self.parse_csv()
                if self.errors:
                    raise ProjectError()
                else:
                    self.fill_project_dict()
        except ProjectError:
            pass  # Just rollback the transaction

    def parse_csv(self):

        last_lexeme_src = None

        for num, data in enumerate(self.csv_reader):

            row = CSVRow(self, num, data, last_lexeme_src)

            if row.num == 0:

                # Header must present, nothing to check
                self.lang_src_cols, self.lang_trg_cols, self.errors = row.parse_csv_header()
                self.colsnum = len(row.data)
                continue

            else:

                self.errors += row.get_ext_comments()

                if len(row.data) != self.colsnum:
                    self.errors += [('Row ' + str(row.num+1), CSVError('CSV-15',
                                                                       'Number of columns: ' + str(len(row.data))))]
                    continue

                self.errors += row.produce_lexeme()
                last_lexeme_src = row.last_lexeme_src

                if not last_lexeme_src:
                    self.errors += [('Row ' + str(row.num+1) + ' (lexemes)', CSVError('CSV-9'))]
                    continue

                self.errors += row.produce_wordforms()

                self.errors += row.produce_translations()

    def fill_project_dict(self):
        project_models = (models.ProjectLexeme, models.ProjectWordform, models.ProjectSemanticGroup)
        for model in project_models:
            src_obj = model.__name__
            for field, term_type in model.project_fields().items():
                if type(term_type) == tuple:
                    term_type = ''
                values = set()
                for value in model.objects.filter(project=self).values(field).distinct():
                    if value[field]:
                        real_value = restore_list(value[field])
                        for sg_value in real_value:
                            values.add(sg_value)
                models.ProjectDictionary.objects.bulk_create(
                    [models.ProjectDictionary(value=val, src_obj=src_obj, project=self, state='N', term_type=term_type)
                     for val in values]
                )

    def produce(self):
        self.errors = []
        try:
            with transaction.atomic():
                if self.state == 'N':
                    for synt_cat in models.ProjectDictionary.\
                            objects.filter(project=self, term_type='SyntacticCategory').values('term_id').distinct():
                        for language in models.ProjectColumn.\
                                objects.filter(project=self).values('language_id').distinct():
                            if not models.SyntCatsInLanguage.is_in(synt_cat['term_id'], language['language_id']):
                                self.errors.append((' '.join([str(synt_cat), str(language)]), TermError('T-1')))
                    if self.errors:
                        raise ProjectError()
                    else:
                        self.produce_project_model(ProjectLexemeProxy)
                        self.produce_project_model(ProjectWordformProxy)
                        self.produce_project_model(ProjectWordformSpellProxy)
                        self.produce_project_model(ProjectSemanticGroupProxy)
                        self.produce_project_model(ProjectTranslationProxy)
                        if self.errors:
                            raise ProjectError()
                        else:
                            self.state = 'P'
                            self.save()
        except ProjectError:
            pass  # Just rollback the transaction

    def produce_project_model(self, model):
        created_objects = []

        for project_object in model.objects.filter(result_id=None, project=self):

            fields = project_object.fields()
            model_object = model.real_model(**fields)
            model_object.save()
            project_object.result = model_object

            m2m_fields = project_object.m2m_fields()
            for m2m_field in m2m_fields:
                # if m2m_fields[m2m_field]:
                # TODO Find out, why NoneType occurs
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

    def clear_produced(self):
        self.delete_produced_object(ProjectTranslationProxy)
        self.delete_produced_object(ProjectSemanticGroupProxy)
        self.delete_produced_object(ProjectWordformSpellProxy)
        self.delete_produced_object(ProjectWordformProxy)
        self.delete_produced_object(ProjectLexemeProxy)
        self.state = 'N'
        self.save()

    def delete_produced_object(self, model):
        for project_object in model.objects.filter(project=self).exclude(result_id=None):
            object_pk = project_object.result_id
            project_object.result_id = None
            project_object.save()
            model.real_model(pk=object_pk).delete()


class CSVRow():

    def __init__(self, project, num, data, last_lexeme_src):
        self.project = project
        self.num = num
        self.data = data
        self.ext_comments = {}
        self.last_lexeme_src = last_lexeme_src

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
            csvcell = CSVCell(rownum=self.num, colnum=self.project.colsnum-1, value=self.data[-1],
                              project=self.project)
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

            self.last_lexeme_src = lexeme_src

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

        params, spelling, transl_dialect, transl_comment, errors = csvcell.split_data(current_transl, True, True,
                                                                                      True)

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


class ProjectedModelMixIn():

    @property
    def params_list(self):
        if self.params:
            return restore_list(self.params)
        else:
            return ()

    def fields(self):
        return {}

    def m2m_fields(self):
        return {}

    def m2m_thru_fields(self):
        return {}

    def get_from_project_dict(self, value, term_type, escape_list=False):
        """
        Gets ID of a term object (from a ProjectDictionary entry) for a ProjectEntity of specific type form a
        specific project.

        :param value: value of a term, parsed from CSV
        :param term_type: name of term class (Term subclass)
        :param escape_list: should be True if a list is passed
        :return: ID of a term object (Term subclass) or None if not found
        """
        if value:
            src_obj = self._meta.proxy_for_model.__name__
            project = self.project
            if escape_list:
                value = value[0]

            if isinstance(value, list):
                dict_items = []
                for real_value in value:
                    try:
                        dict_items.append(models.ProjectDictionary.objects.get(value=real_value, src_obj=src_obj,
                                                                               term_type=term_type,
                                                                               project=project).term_id)
                    except ObjectDoesNotExist:
                        print(src_obj, project, real_value, term_type)
                        pass  # Really nothing to do
            else:
                try:
                    dict_items = models.ProjectDictionary.objects.get(value=value, src_obj=src_obj,
                                                                      term_type=term_type, project=project).term_id
                except ObjectDoesNotExist:
                    print(src_obj, project, value, term_type)
                    return None

        else:
            return None

        return dict_items

    class Meta:
        abstract = True


class ProjectLexemeProxy(models.ProjectLexeme, ProjectedModelMixIn):
    real_model = models.Lexeme

    class Meta:
        proxy = True

    @staticmethod
    def project_fields():
        return {'syntactic_category': 'SyntacticCategory', 'params': ('Inflection', 'LexemeParameter')}

    def fields(self):
        fields = {'syntactic_category_id': self.get_from_project_dict(self.syntactic_category, 'SyntacticCategory'),
                  'language': self.col.language}
        if self.params_list:
            fields['inflection'] = self.get_from_project_dict(self.params_list, 'Inflection', True)
        return fields

    def m2m_fields(self):
        m2m_fields = {}
        if self.params_list:
            m2m_fields['lexeme_parameter_m'] = self.get_from_project_dict(self.params_list, 'LexemeParameter')
        return m2m_fields


class ProjectWordformProxy(models.ProjectWordform, ProjectedModelMixIn):
    real_model = models.Wordform

    class Meta:
        proxy = True

    @staticmethod
    def project_fields():
        return {'params': ('GrammCategorySet', 'Dialect')}

    def fields(self):
        fields = {'lexeme': self.lexeme.result, 'writing_type': self.col.writing_system.writing_type}
        if self.params_list:
            fields['gramm_category_set_id'] = self.get_from_project_dict(self.params_list, 'GrammCategorySet', True)
        if not fields.get('gramm_category_set_id'):
            fields['gramm_category_set'] = self.col.language.get_main_gr_cat(self.lexeme.result.syntactic_category)
            if 'gramm_category_set_id' in fields.keys():
                del fields['gramm_category_set_id']  # Without deletion conflicting keys present

        return fields

    def m2m_fields(self):
        m2m_fields = {}
        if self.params_list:
            m2m_fields['dialect_m'] = self.get_from_project_dict(self.params_list, 'Dialect')
        if not m2m_fields.get('dialect_m'):
            m2m_fields['dialect_m'] = [self.col.dialect_id]
        return m2m_fields

    def m2m_thru_fields(self):
        return {models.DictWordform: {'source': self.project.source, 'wordform': self.result, 'comment': self.comment,
                                      'is_deleted': False}}


class ProjectWordformSpellProxy(models.ProjectWordformSpell, ProjectedModelMixIn):
    real_model = models.WordformSpell

    class Meta:
        proxy = True

    def fields(self):
        return {'wordform': self.wordform.result, 'spelling': self.spelling, 'writing_system': self.col.writing_system,
                'is_processed': self.is_processed}


class ProjectSemanticGroupProxy(models.ProjectSemanticGroup, ProjectedModelMixIn):
    real_model = models.SemanticGroup

    class Meta:
        proxy = True

    @staticmethod
    def project_fields():
        return {'params': ('Dialect', 'Theme', 'UsageConstraint'), 'dialect': 'Dialect'}

    @property
    def dialect_list(self):
        if self.dialect:
            return restore_tuple(self.dialect)
        else:
            return []

    def fields(self):
        return {'comment': self.comment}

    def m2m_fields(self):
        m2m_fields = {}
        if self.dialect_list:
            m2m_fields['dialect_m'] = self.get_from_project_dict(self.dialect_list, 'Dialect')
        if self.params_list:
            m2m_fields['dialect_m'] = self.get_from_project_dict(self.params_list, 'Dialect')
            m2m_fields['theme_m'] = self.get_from_project_dict(self.params_list, 'Theme')
            m2m_fields['usage_constraint_m'] = self.get_from_project_dict(self.params_list, 'UsageConstraint')
        return m2m_fields

    def m2m_thru_fields(self):
        return {models.DictSemanticGroup: {'source': self.project.source, 'semantic_group': self.result,
                                           'is_deleted': False}}


class ProjectTranslationProxy(models.ProjectTranslation, ProjectedModelMixIn):
    real_model = models.Translation

    class Meta:
        proxy = True

    def fields(self):
        return {'lexeme_1': self.lexeme_1.result, 'lexeme_2': self.lexeme_2.result, 'direction': self.direction,
                'semantic_group_1': self.semantic_group_1.result, 'semantic_group_2': self.semantic_group_2.result}

    def m2m_thru_fields(self):
        return {models.DictTranslation: {'source': self.project.source, 'translation': self.result,
                                         'is_deleted': False}}