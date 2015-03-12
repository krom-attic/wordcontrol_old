import string

from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from wordengine.commonworks import *


# System globals. Abstract


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(User, editable=False, related_name="%(app_label)s_%(class)s_changer")
    timestamp_change = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(blank=True)
    # TODO Check change generating code - it wasn't changed
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


# System globals. Concrete


class DictChange(Change):
    """This class extends Change class with fields representing change review and information source for
     Wordforms and Translations"""

    user_reviewer = models.ForeignKey(User, editable=False, null=True, blank=True)
    timestamp_review = models.DateTimeField(editable=False, null=True, blank=True)


class FieldChange(Change):
    """This class extends Change class with fields representing field change"""

    field_name = models.CharField(max_length=256)
    old_value = models.CharField(max_length=512, blank=True)
    new_value = models.CharField(max_length=512, blank=True)


class ChangeTrackMixIn(object):
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


    # TODO Log every change - overload save() method? (Add dict_change)
    #                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
    #                                                     object_id=wordform.id)
    #                     dict_change.save()

        # dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
        #                                 object_id=translation.id)
        # dict_change.save()


class Settings(models.Model):

    pass


# Global lists. Abstract


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64, blank=True)  # TODO May be it should be unique???
    description = models.TextField(blank=True)

    def __str__(self):
        return self.term_full

    class Meta:
        abstract = True


# Global lists. Concrete


class LexemeParameter(Term):
    """Temporary class for lexeme parameters"""

    pass


class SyntacticCategory(Term):
    """Class represents syntactic category (used in lexemes) list"""

    pass


class UsageConstraint(Term):
    """Class represents usage constraints (used in translations) list"""

    pass


class Theme(Term):
    """ Class for translation themes
    """

    pass


class GrammCategoryType(Term):
    """Class represents types of grammatical categories"""

    pass


class GrammCategory(Term):
    """Class represents values list for grammatical categories"""

    gramm_category_type = models.ForeignKey(GrammCategoryType)
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.gramm_category_type)])


class Language(Term):
    """Class represents languages present in the system"""

    syntactic_category_m = models.ManyToManyField(SyntacticCategory, through='SyntCatsInLanguage',
                                                  through_fields=('language', 'syntactic_category'),
                                                  null=True, blank=True, related_name='synt_cat_set')
    iso_code = models.CharField(max_length=8)  # ISO 639-3

    def get_main_gr_cat(self, synt_cat):
        return self.syntcatsinlanguage_set.get(syntactic_category=synt_cat).main_gramm_category_set


# Language-dependant classes. Abstract


class LanguageEntity(models.Model):
    """Abstract base class used to tie an entity to a language"""

    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


# Language-dependant classes. Concrete


class Dialect(Term, LanguageEntity):
    """Class represents dialect present in the system"""

    parent_dialect = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])


class WritingRelated(models.Model):
    writing_type = models.CharField(choices=WS_TYPE, max_length=2)

    class Meta:
        abstract = True


class WritingSystem(Term, WritingRelated):
    """Class represents a writing systems used to spell a word form"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"


class Source(Term, LanguageEntity):
    """Class representing sources of language information"""

    source_type = models.CharField(choices=SRC_TYPE, max_length=2)


class GrammCategorySet(LanguageEntity):
    """Class represents possible composite sets of grammar categories and its order in a given language
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    gramm_category_m = models.ManyToManyField(GrammCategory)
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
            return ' '.join(str(s) for s in self.gramm_category_m.all())

    class Meta:
        unique_together = ('language', 'position')


class SyntCatsInLanguage(models.Model):
    language = models.ForeignKey(Language)
    syntactic_category = models.ForeignKey(SyntacticCategory)
    main_gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)

    @staticmethod
    def is_in(synt_cat, language):
        try:
            return SyntCatsInLanguage.objects.get(language=language, syntactic_category=synt_cat)
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return ' '.join((str(self.language), str(self.syntactic_category) + ':', str(self.main_gramm_category_set)))


class Inflection(LanguageEntity):

    syntactic_category = models.ForeignKey(SyntacticCategory)
    value = models.CharField(max_length=512)


class Lexeme(LanguageEntity):
    """Class representing current lexemes
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    inflection = models.ForeignKey(Inflection, null=True, blank=True)
    lexeme_parameter_m = models.ManyToManyField(LexemeParameter, null=True, blank=True)
    translation_m = models.ManyToManyField('self', symmetrical=False, through='Translation', null=True, blank=True,
                                           related_name='translation_set')
    lexeme_relation_m = models.ManyToManyField('self', symmetrical=False, through='Relation', null=True, blank=True,
                                               related_name='relation_set')
    # TODO Add field for a dictionary wordform
    # Absence of a dialectical dependency is intentional

    @property
    def spellings(self):
        return self.wordform_set.filter(writing_type='O')

    @property
    def transcriptions(self):
        return self.wordform_set.filter(writing_type__in=['PS', 'PL'])

    @property
    def lexeme_short(self):
        if self.spellings.first():
            title_wordform = self.spellings.first().default_formatted
        elif self.transcriptions.first():
            title_wordform = self.transcriptions.first().default_formatted
        else:
            title_wordform = '[No wordform attached]'
        return title_wordform

    @property
    def lexeme_title(self):
        lexeme_title = ''
        if self.spellings.first():
            lexeme_title = self.spellings.first().default_formatted
        if self.transcriptions.first():
            ' '.join([lexeme_title, self.transcriptions.first().default_formatted]).strip()
        if not lexeme_title:
            return '[No wordform attached]'
        return lexeme_title

    def __str__(self):
        return ' | '.join(str(s) for s in [self.lexeme_short,  self.language, self.syntactic_category])


class TranslatedTerm(LanguageEntity):
    """Class representing term translation for the given language"""

    table = models.CharField(max_length=256)
    term_id = models.IntegerField()
    term_full_translation = models.CharField(max_length=256)
    term_abbr_translation = models.CharField(max_length=64, blank=True)


# Dictionary classes. Abstract


class DictEntity(models.Model):
    source = models.ForeignKey(Source)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class LexemeRelation(models.Model):
    """ Class for lexemes' special relations
    """

    direction = models.CharField(choices=REL_DIRECTION, max_length=1)

    class Meta:
        abstract = True


# Dictionary classes. Concrete


class Wordform(WritingRelated):
    """Class representing current wordforms"""

    lexeme = models.ForeignKey(Lexeme, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)
    source_m = models.ManyToManyField(Source, through='DictWordform')
    dialect_m = models.ManyToManyField(Dialect, null=True, blank=True)
    # informant = models.CharField(max_length=256, blank=True)

    @property
    def default_spell(self):
        return self.wordformspell_set.get(is_processed=False)

    @property
    def processed_spells(self):
        return self.wordformspell_set.filter(is_processed=True)

    @property
    def default_formatted(self):
        return self.default_spell.formatted

    @property
    def processed_formatted_all(self):
        spellings = [spell.formatted for spell in self.processed_spells]
        if spellings:
            result = spellings.pop(0)
            for spelling in spellings:
                result += ', '
                result += spelling
            return result
        else:
            return ''

    @property
    def dialects(self):
        if self.dialect_m.first():
            return ', '.join(str(s) for s in self.dialect_m.all())

    @property
    def is_deleted(self):
        return self.default_spell.is_deleted

    def __str__(self):
        return '{0} ({1} {2}) | {3}'.format(self.default_formatted, str(self.lexeme.language),
                                            str(self.gramm_category_set), str(self.writing_type))
    # TODO Include dialects into description


class WordformSpell(models.Model):
    wordform = models.ForeignKey(Wordform)
    spelling = models.CharField(max_length=512)
    writing_system = models.ForeignKey(WritingSystem)
    is_processed = models.BooleanField()

    @property
    def formatted(self):
        if self.writing_system.writing_type == 'O':
            return self.spelling
        else:
            return TRANSCRIPT_BRACKETS[self.writing_system.writing_type].format(self.spelling)

    def __str__(self):
        return self.formatted

class DictWordform(DictEntity):
    wordform = models.ForeignKey(Wordform)
    comment = models.TextField(blank=True)


class WordformOrder:

    pass


class SemanticGroup(models.Model):
    """ Class representing semantic groups
    """
    theme_m = models.ManyToManyField(Theme, null=True, blank=True)
    usage_constraint_m = models.ManyToManyField(UsageConstraint, null=True, blank=True)
    dialect_m = models.ManyToManyField(Dialect, null=True, blank=True)
    source_m = models.ManyToManyField(Source, through='DictSemanticGroup')
    comment = models.TextField(blank=True)

    def __str__(self):
        semantic_group_str = ''
        themes = self.theme_m.all()
        if themes:
            semantic_group_str += ','.join(themes) + ' | '
        usage_contraint = self.usage_constraint_m.all()
        if usage_contraint:
            semantic_group_str += ';'.join(usage_contraint) + ' | '
        dialects = self.dialect_m.all()
        if dialects:
            semantic_group_str += ','.join(dialects) + ' | '
        if self.comment:
            semantic_group_str += self.comment

        if semantic_group_str:
            semantic_group_str = semantic_group_str.strip(' | ')

        return semantic_group_str


class DictSemanticGroup(DictEntity):
    semantic_group = models.ForeignKey(SemanticGroup)


class Translation(LexemeRelation):
    """Class representing current translations
    """

    lexeme_1 = models.ForeignKey(Lexeme, related_name='translation_fst_set')
    lexeme_2 = models.ForeignKey(Lexeme, related_name='translation_snd_set')
    semantic_group_1 = models.ForeignKey(SemanticGroup, related_name='translation_fst_set')
    semantic_group_2 = models.ForeignKey(SemanticGroup, related_name='translation_snd_set')
    wordform_1 = models.ForeignKey(Wordform, null=True, blank=True, related_name='translation_fst_set')
    wordform_2 = models.ForeignKey(Wordform, null=True, blank=True, related_name='translation_snd_set')
    source_m = models.ManyToManyField(Source, through='DictTranslation')
    #  TODO: may be these fields should be moved to another class, deliberately made for overlying dictionary
    # translation_based_m = models.ManyToManyField('self', null=True, blank=True)
    # is_visible = models.BooleanField(default=True, editable=False)

    # def __str__(self):
    #     return


class DictTranslation(DictEntity):
    translation = models.ForeignKey(Translation)


class Relation(LexemeRelation):
    """Class representing lexeme relations
    """

    lexeme_1 = models.ForeignKey(Lexeme, related_name='relation_fst_set')
    lexeme_2 = models.ForeignKey(Lexeme, related_name='relation_snd_set')
    wordform_1 = models.ForeignKey(Wordform, null=True, blank=True, related_name='relation_fst_set')
    wordform_2 = models.ForeignKey(Wordform, null=True, blank=True, related_name='relation_snd_set')
    relation_type = models.CharField(max_length=32)
    # source = models.ManyToManyField(Source, through='DictRelation')
    # TODO Will not work due to m2m-relation to source isn't set


# Project classes


class Project(models.Model):
    user_uploader = models.ForeignKey(User, editable=False)
    timestamp_upload = models.DateTimeField(auto_now_add=True, editable=False)
    filename = models.CharField(max_length=512)
    source = models.ForeignKey(Source, null=True, blank=True)
    state = models.CharField(choices=PRJ_STATE, max_length=2)  # Project state is excessive, but can't be removed now

    def __str__(self):
        return 'Project #{0} by {1} @ {2}'.format(str(self.id), self.user_uploader, self.timestamp_upload)

    def get_absolute_url(self):
        return reverse('wordengine:project_setup', kwargs={'pk': self.pk})


class ProjectCSVCell(models.Model):
    rownum = models.PositiveIntegerField()
    colnum = models.PositiveSmallIntegerField()
    value = models.TextField(blank=True)
    project = models.ForeignKey(Project)

    @property
    def excel_cell_code(self):
        # Here may occur an out-of-range error, but it is not rational to handle it
        return string.ascii_uppercase[self.colnum] + str(self.rownum+1)

    def __str__(self):
        return 'Cell {0} ({1})'.format(self.excel_cell_code, self.value)


class ProjectedEntity(models.Model):
    project = models.ForeignKey(Project)
    state = models.CharField(choices=PRJ_STATE, max_length=2)

    class Meta:
        abstract = True


class SrcImg(ProjectedEntity):
    # img = models.ImageField()  # import pillow!
    filename = models.CharField(max_length=256)


class RawTextData(ProjectedEntity):
    text = models.TextField(blank=True)


class ImgData(ProjectedEntity):
    img = models.ForeignKey(SrcImg)
    text = models.ForeignKey(RawTextData)
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    h = models.SmallIntegerField()
    w = models.SmallIntegerField()


class ProjectDictionary(ProjectedEntity):
    value = models.CharField(max_length=256)
    src_obj = models.CharField(max_length=256)
    # src_field = models.CharField(max_length=256, null=True, blank=True)

    term_type = models.CharField(max_length=128, blank=True)
    term_id = models.PositiveIntegerField(null=True, blank=True)
    # term_type = models.ForeignKey(ContentType, null=True, blank=True)
    # term_id = models.PositiveIntegerField(null=True, blank=True)
    # content_object = GenericForeignKey('term_type', 'term_id')

    class Meta:
        unique_together = ('value', 'src_obj', 'term_type', 'project')


class ProjectColumn(ProjectedEntity):
    # TODO State field seems to be redundant
    language_l = models.CharField(max_length=256)
    dialect_l = models.CharField(max_length=256, blank=True)
    # source_l = models.CharField(max_length=256, null=True, blank=True)
    writing_system_l = models.CharField(max_length=256, blank=True)
    num = models.SmallIntegerField()
    csvcell = models.ForeignKey(ProjectCSVCell)

    language = models.ForeignKey(Language, null=True, blank=True)
    dialect = models.ForeignKey(Dialect, null=True, blank=True)
    # source = models.ForeignKey(Source, null=True, blank=True)
    writing_system = models.ForeignKey(WritingSystem, null=True, blank=True)

    def __str__(self):
        return 'Col #{0}: {1}'.format(str(self.num), self.csvcell)


class ProjectedModel (models.Model):

    @property
    def params_list(self):
        if self.params:
            return restore_tuple(self.params)
        else:
            return ()

    def fields(self):
        return {}

    def m2m_fields(self):
        return {}

    def m2m_thru_fields(self):
        return {}

    class Meta:
        abstract = True


def get_from_project_dict(obj, value, term_type, escape_list=False):
    if value:
        src_obj = type(obj).__name__
        project = obj.project
        if escape_list:
            value = value[0]

        if isinstance(value, list):
            dict_items = []
            for real_value in value:
                try:
                    dict_items.append(ProjectDictionary.objects.get(value=real_value, src_obj=src_obj,
                                                                    term_type=term_type, project=project).term_id)
                except ObjectDoesNotExist:
                    pass  # Really nothing to do
        else:
            try:
                dict_items = ProjectDictionary.objects.get(value=value, src_obj=src_obj,
                                                           term_type=term_type, project=project).term_id
            except ObjectDoesNotExist:
                return None

    else:
        return None

    return dict_items


class ProjectLexeme(ProjectedEntity, ProjectedModel):
    syntactic_category = models.CharField(max_length=256)
    params = models.CharField(max_length=512, blank=True)
    col = models.ForeignKey(ProjectColumn)
    csvcell = models.ForeignKey(ProjectCSVCell)
    result = models.ForeignKey(Lexeme, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([self.syntactic_category, str(self.params)])

    @staticmethod
    def real_model():
        return Lexeme

    @staticmethod
    def project_fields():
        return {'syntactic_category': 'SyntacticCategory', 'params': ('Inflection', 'LexemeParameter')}

    def fields(self):
        fields = {'syntactic_category_id': get_from_project_dict(self, self.syntactic_category, 'SyntacticCategory'),
                  'language': self.col.language}
        if self.params_list:
            fields['inflection'] = get_from_project_dict(self, self.params_list, 'Inflection', True)
        return fields

    def m2m_fields(self):
        m2m_fields = {}
        if self.params_list:
            m2m_fields['lexeme_parameter_m'] = get_from_project_dict(self, self.params_list, 'LexemeParameter')
        return m2m_fields


class ProjectWordform(ProjectedEntity, ProjectedModel):
    lexeme = models.ForeignKey(ProjectLexeme)
    comment = models.TextField(blank=True)
    params = models.CharField(max_length=512, blank=True)
    col = models.ForeignKey(ProjectColumn)
    csvcell = models.ForeignKey(ProjectCSVCell)
    result = models.ForeignKey(Wordform, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.lexeme), self.spelling, self.comment, str(self.params)])

    @staticmethod
    def real_model():
        return Wordform

    @staticmethod
    def project_fields():
        return {'params': ('GrammCategorySet', 'Dialect')}

    def fields(self):
        fields = {'lexeme': self.lexeme.result}
        if self.params_list:
            fields['gramm_category_set_id'] = get_from_project_dict(self, self.params_list, 'GrammCategorySet', True)
        if not fields.get('gramm_category_set_id'):
            fields['gramm_category_set'] = self.col.language.get_main_gr_cat(self.lexeme.result.syntactic_category)
            if 'gramm_category_set_id' in fields.keys():
                del fields['gramm_category_set_id']  # Without deletion conflicting keys present

        return fields

    def m2m_fields(self):
        m2m_fields = {}
        if self.params_list:
            m2m_fields['dialect_m'] = get_from_project_dict(self, self.params_list, 'Dialect')
        if not m2m_fields.get('dialect_m'):
            m2m_fields['dialect_m'] = [self.col.dialect_id]
        return m2m_fields

    def m2m_thru_fields(self):
        return {DictWordform: {'source': self.project.source, 'wordform': self.result, 'comment': self.comment,
                               'is_deleted': False}}


class ProjectWordformSpell(ProjectedEntity, ProjectedModel):
    wordform = models.ForeignKey(ProjectWordform)
    is_processed = models.BooleanField()
    spelling = models.CharField(max_length=256)
    col = models.ForeignKey(ProjectColumn)
    csvcell = models.ForeignKey(ProjectCSVCell)
    result = models.ForeignKey(WordformSpell, null=True, blank=True)

    @staticmethod
    def real_model():
        return WordformSpell

    def fields(self):
        return {'wordform': self.wordform.result, 'spelling': self.spelling, 'writing_system': self.col.writing_system,
                'is_processed': self.is_processed}


class ProjectSemanticGroup(ProjectedEntity, ProjectedModel):
    params = models.CharField(max_length=256, blank=True)  # For the source side there can be a dialect or a theme
    dialect = models.CharField(max_length=256, blank=True)  # For the target side it is only a dialect possible
    comment = models.TextField(blank=True)
    # col = models.ForeignKey(ProjectColumn, null=True, blank=True)
    csvcell = models.ForeignKey(ProjectCSVCell)
    result = models.ForeignKey(SemanticGroup, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.params), self.dialect, self.comment])

    @staticmethod
    def real_model():
        return SemanticGroup

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
            m2m_fields['dialect_m'] = get_from_project_dict(self, self.dialect_list, 'Dialect')
        if self.params_list:
            m2m_fields['dialect_m'] = get_from_project_dict(self, self.params_list, 'Dialect')
            m2m_fields['theme_m'] = get_from_project_dict(self, self.params_list, 'Theme')
            m2m_fields['usage_constraint_m'] = get_from_project_dict(self, self.params_list, 'UsageConstraint')
        return m2m_fields

    def m2m_thru_fields(self):
        return {DictSemanticGroup: {'source': self.project.source, 'semantic_group': self.result, 'is_deleted': False}}


class ProjectTranslation(ProjectedEntity, ProjectedModel):
    lexeme_1 = models.ForeignKey(ProjectLexeme, related_name='translation_fst_set')
    lexeme_2 = models.ForeignKey(ProjectLexeme, related_name='translation_snd_set')
    direction = models.SmallIntegerField()
    semantic_group_1 = models.ForeignKey(ProjectSemanticGroup,  related_name='translation_fst_set')
    semantic_group_2 = models.ForeignKey(ProjectSemanticGroup,  related_name='translation_snd_set')
    # wordform_1 = models.ForeignKey(ProjectWordform, related_name='translation_fst_set')
    # wordform_2 = models.ForeignKey(ProjectWordform, related_name='translation_snd_set')
    result = models.ForeignKey(Translation, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.lexeme_1), str(self.lexeme_2), str(self.direction), str(self.semantic_group_1),
    #                        str(self.semantic_group_2), str(self.bind_wf_1), str(self.bind_wf_2)])

    @staticmethod
    def real_model():
        return Translation

    def fields(self):
        return {'lexeme_1': self.lexeme_1.result, 'lexeme_2': self.lexeme_2.result, 'direction': self.direction,
                'semantic_group_1': self.semantic_group_1.result, 'semantic_group_2': self.semantic_group_2.result}

    def m2m_thru_fields(self):
        return {DictTranslation: {'source': self.project.source, 'translation': self.result, 'is_deleted': False}}