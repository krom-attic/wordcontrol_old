from wordengine.commonworks import *
from wordengine import models
from wordengine.specials import csvworks

from django.db import transaction


class ProjectProxy(models.Project):

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(ProjectProxy, self).__init__(*args, **kwargs)
        # Errors storage format: whole data, error code, erroneous fragment (optional)
        self.errors = []

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
        return None

    def produce_project_model(self, model):
        created_objects = []

        for project_object in model.objects.filter(state='N', project=self):

            fields = project_object.fields()
            model_object = model.real_model()(**fields)
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

    def produce_project(self):
        transaction.set_autocommit(False)
        errors = []
        if self.state == 'N':
            for synt_cat in models.ProjectDictionary.objects.filter(project=self, term_type='SyntacticCategory').\
                    values('term_id').distinct():
                for language in models.ProjectColumn.objects.filter(project=self).values('language_id').distinct():
                    if not models.SyntCatsInLanguage.is_in(synt_cat['term_id'], language['language_id']):
                        errors.append((' '.join([synt_cat, language]), TermError('T-1')))
            self.produce_project_model(models.ProjectLexeme)
            self.produce_project_model(models.ProjectWordform)
            self.produce_project_model(models.ProjectWordformSpell)
            self.produce_project_model(models.ProjectSemanticGroup)
            self.produce_project_model(models.ProjectTranslation)
            if not errors:
                self.state = 'P'
                self.save()
        transaction.set_autocommit(True)
        return errors

    def parse_csv(self, csvreader):

        self.save()  # Required

        for num, data in enumerate(csvreader):

            row = csvworks.CSVRow(self, num, data)

            if row.num == 0:

                # Header must present, nothing to check
                self.lang_src_cols, self.lang_trg_cols, self.errors = row.parse_csv_header()
                self.colsnum = len(row.data)
                continue

            else:

                self.errors += row.get_ext_comments()

                self.errors += row.produce_lexeme()

                if not row.last_lexeme_src:
                    self.errors += [('Row ' + str(row.num+1) + ' (lexemes)', CSVError('CSV-9'), )]
                    continue

                self.errors += row.produce_wordforms()

                self.errors += row.produce_translations()

        csvworks.CSVRow.last_lexeme_src = None

        return None


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