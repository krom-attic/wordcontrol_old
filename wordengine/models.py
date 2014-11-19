from django.db import models
from django.contrib import auth
from wordengine.global_const import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# System globals. Abstract


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(auth.models.User, editable=False, related_name="%(app_label)s_%(class)s_changer")
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

    user_reviewer = models.ForeignKey(auth.models.User, editable=False, null=True, blank=True)
    timestamp_review = models.DateTimeField(editable=False, null=True, blank=True)


class FieldChange(Change):
    """This class extends Change class with fields representing field change"""

    field_name = models.CharField(max_length=256)
    old_value = models.CharField(max_length=512, blank=True)
    new_value = models.CharField(max_length=512, blank=True)


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

    syntactic_category_m = models.ManyToManyField(SyntacticCategory, null=True, blank=True)
    iso_code = models.CharField(max_length=8)  # ISO 639-3


# Language-dependant classes. Abstract


class LanguageRelated(models.Model):

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"

    class Meta:
        abstract = True


class LanguageEntity(models.Model):
    """Abstract base class used to tie an entity to a language"""

    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


# Language-dependant classes. Concrete


class Dialect(Term, LanguageRelated):
    """Class represents dialect present in the system"""

    parent_dialect = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])


class WritingSystem(Term, LanguageRelated):
    """Class represents a writing systems used to spell a word form"""

    writing_system_type = models.CharField(choices=WS_TYPE, max_length=2)


class Source(Term, LanguageRelated):
    """Class representing sources of language information"""

    source_type = models.CharField(choices=SRC_TYPE, max_length=2)
    source_parent = models.ForeignKey('self', null=True, blank=True)
    processing_type = models.CharField(choices=PROC_TYPE, max_length=2)
    processing_comment = models.TextField(blank=True)


# TODO Source handling seems to be lame

class GrammCategorySet(LanguageEntity):
    """Class represents possible composite sets of grammar categories and its order in a given language
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    gramm_category_m = models.ManyToManyField(GrammCategory)  # TODO: Fix string display due to this change
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
            return ' '.join(str(s) for s in self.gramm_category_multi.all())

    class Meta:
        unique_together = ('language', 'position')


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
        return self.wordform_set.filter(writing_system__writing_system_type=3)

    @property
    def transcriptions(self):
        return self.wordform_set.filter(writing_system__writing_system_type__in=[1, 2])

    def __str__(self):
        if self.spellings.first():
            title_wordform = self.spellings.first().formatted
        elif self.transcriptions.first():
            title_wordform = self.transcriptions.first().formatted
        else:
            title_wordform = '[No wordform attached]'
        return ' | '.join(str(s) for s in [title_wordform,  self.language, self.syntactic_category])


class TranslatedTerm(LanguageEntity):
    """Class representing term translation for the given language"""

    table = models.CharField(max_length=256)
    term_id = models.IntegerField()
    term_full_translation = models.CharField(max_length=256)
    term_abbr_translation = models.CharField(max_length=64, blank=True)


# Dictionary classes. Abstract


class DictEntity(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    comment = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class LexemeRelation(models.Model):
    """ Class for lexemes' special relations
    """

    direction = models.CharField(choices=REL_DIRECTION, max_length=1)

    class Meta:
        abstract = True


class WordformBase(models.Model):
    """Base class for wordforms
    """

    lexeme = models.ForeignKey(Lexeme, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)
    spelling = models.CharField(max_length=512)
    writing_system = models.ForeignKey(WritingSystem)
    source_m = models.ManyToManyField(Source, through='DictWordform')

    @property
    def formatted(self):
        if self.writing_system:
            try:
                return self.TRANSCRIPT_BRACKETS[self.writing_system.writing_system_type.id].format(self.spelling)
            except KeyError:
                return self.spelling
        else:
            return self.spelling

    @property
    def ws(self):
        return str(self.writing_system)

    class Meta:
        abstract = True


# Dictionary classes. Concrete


class Wordform(WordformBase):
    """Class representing current wordforms"""

    dialect_m = models.ManyToManyField(Dialect, null=True, blank=True)

    @property
    def dialects(self):
        if self.dialect_multi.first():
            return ', '.join(str(s) for s in self.dialect_multi.all())

    def __str__(self):
        try:
            ws = str(self.writing_system.term_abbr)
        except AttributeError:
            ws = ""
        return '{0} ({1} {2}) | {3}'.format(self.spelling, str(self.lexeme.language), str(self.gramm_category_set), ws)
    #TODO Include dialects into description


class DictWordform(DictEntity):
    wordform = models.ForeignKey(Wordform)


# TODO Will not work due to m2m-relation to source via DictWordform
# class WordformSample(WordformBase):
#     """Class representing current wordform samples"""
#
#     informant = models.CharField(max_length=256)


class WordformOrder:

    pass


class SemanticGroup(models.Model):
    """ Class representing semantic groups
    """
    theme_m = models.ManyToManyField(Theme, null=True, blank=True)
    usage_constraint_m = models.ManyToManyField(UsageConstraint, null=True, blank=True)
    dialect_m = models.ManyToManyField(Dialect, null=True, blank=True)
    source_m = models.ManyToManyField(Source, through='DictSemanticGroup')


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
    user_uploader = models.ForeignKey(auth.models.User, editable=False)
    timestamp_upload = models.DateTimeField(auto_now_add=True, editable=False)
    filename = models.CharField(max_length=512)

    def __str__(self):
        return 'Project #{0} by {1} @ {2}'.format(str(self.id), self.user_uploader, self.timestamp_upload)


class CSVCell(models.Model):
    row = models.IntegerField()
    col = models.SmallIntegerField()
    value = models.TextField(blank=True)
    project = models.ForeignKey(Project)


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
    src_field = models.CharField(max_length=256)

    term_type = models.CharField(max_length=128, null=True, blank=True)
    term_id = models.PositiveIntegerField(null=True, blank=True)
    # term_type = models.ForeignKey(ContentType, null=True, blank=True)
    # term_id = models.PositiveIntegerField(null=True, blank=True)
    # content_object = GenericForeignKey('term_type', 'term_id')

    class Meta:
        unique_together = ('value', 'src_obj', 'src_field', 'project')


class ProjectColumn(ProjectedEntity):
    language_l = models.CharField(max_length=256)
    dialect_l = models.CharField(max_length=256, null=True, blank=True)
    source_l = models.CharField(max_length=256, null=True, blank=True)
    writing_system_l = models.CharField(max_length=256, null=True, blank=True)
    processing_l = models.CharField(max_length=256, null=True, blank=True)
    num = models.SmallIntegerField()
    csvcell = models.ForeignKey(CSVCell)

    language = models.ForeignKey(Language, null=True, blank=True)
    dialect = models.ForeignKey(Dialect, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)
    writing_system = models.ForeignKey(WritingSystem, null=True, blank=True)
    processing_type = models.CharField(choices=PROC_TYPE, max_length=2, null=True, blank=True)
    processing_comment = models.TextField(blank=True)


class ProjectedModel (models.Model):

    @staticmethod
    def fixed_fks():
        return {}

    @staticmethod
    def fixed_m2ms():
        return {}

    @staticmethod
    def param_fks():
        return {}

    @staticmethod
    def param_m2ms():
        return {}

    @classmethod
    def project_fields(cls):
        if cls.param_fks() or cls.param_m2ms():
            project_fields = ['params']
        else:
            project_fields = []
        project_fields.extend(cls.fixed_fks().values())
        project_fields.extend(cls.fixed_m2ms().values())
        return project_fields

    def known_fks(self):
        pass

    class Meta:
        abstract = True


class ProjectLexeme(ProjectedEntity, ProjectedModel):
    syntactic_category = models.CharField(max_length=256)
    params = models.CharField(max_length=512, blank=True)
    col = models.ForeignKey(ProjectColumn, null=True, blank=True)
    csvcell = models.ForeignKey(CSVCell)
    result = models.ForeignKey(Lexeme, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([self.syntactic_category, str(self.params)])

    @staticmethod
    def real_model():
        return Lexeme

    @staticmethod
    def fixed_fks():
        return {'SyntacticCategory': 'syntactic_category'}

    @staticmethod
    def param_fks():
        return {'Inflection': 'inflection'}

    @staticmethod
    def param_m2ms():
        return {'LexemeParameter': 'lexeme_parameter_m'}

    def known_fks(self):
        return {'language': self.col.language}


class ProjectWordform(ProjectedEntity, ProjectedModel):
    lexeme = models.ForeignKey(ProjectLexeme)
    spelling = models.CharField(max_length=256)
    comment = models.TextField(blank=True)
    params = models.CharField(max_length=512, blank=True)
    col = models.ForeignKey(ProjectColumn, null=True, blank=True)
    csvcell = models.ForeignKey(CSVCell)
    result = models.ForeignKey(Wordform, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.lexeme), self.spelling, self.comment, str(self.params)])

    @staticmethod
    def real_model():
        return Wordform

    @staticmethod
    def param_fks():
        return {'GrammCategorySet': 'gramm_category_set'}

    @staticmethod
    def param_m2ms():
        return {'Dialect': 'dialect_m'}

    def known_fks(self):
        return {'lexeme': self.lexeme.result, 'writing_system': self.col.writing_system}

    def known_m2ms(self):
        return {'source': self.col.source, 'dialect': self.col.dialect}


class ProjectSemanticGroup(ProjectedEntity, ProjectedModel):
    params = models.CharField(max_length=256, blank=True)  # For the source side there can be a dialect or a theme
    dialect = models.CharField(max_length=256, blank=True)  # For the target side it is only a dialect possible
    comment = models.TextField(blank=True)
    csvcell = models.ForeignKey(CSVCell)
    result = models.ForeignKey(SemanticGroup, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.params), self.dialect, self.comment])

    @staticmethod
    def real_model():
        return SemanticGroup

    @staticmethod
    def fixed_m2ms():
        return {'Dialect': 'dialect_m'}

    @staticmethod
    def param_m2ms():
        return {'Dialect': 'dialect_m', 'Theme': 'theme_m', 'UsageConstraint': 'usage_constraint_m'}


class ProjectTranslation(ProjectedEntity, ProjectedModel):
    lexeme_1 = models.ForeignKey(ProjectLexeme, related_name='translation_fst_set')
    lexeme_2 = models.ForeignKey(ProjectLexeme, related_name='translation_snd_set')
    direction = models.SmallIntegerField()
    semantic_group_1 = models.ForeignKey(ProjectSemanticGroup,  related_name='translation_fst_set')
    semantic_group_2 = models.ForeignKey(ProjectSemanticGroup,  related_name='translation_snd_set')
    bind_wf_1 = models.ForeignKey(ProjectWordform, related_name='translation_fst_set')
    bind_wf_2 = models.ForeignKey(ProjectWordform, related_name='translation_snd_set')
    result = models.ForeignKey(Translation, null=True, blank=True)

    # def __str__(self):
    #     return ' | '.join([str(self.lexeme_1), str(self.lexeme_2), str(self.direction), str(self.semantic_group_1),
    #                        str(self.semantic_group_2), str(self.bind_wf_1), str(self.bind_wf_2)])

    @staticmethod
    def real_model():
        return Translation