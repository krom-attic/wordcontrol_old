from django.db import models
from django.contrib import auth
from django.db.models import Q


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(auth.models.User, editable=False, related_name="%(app_label)s_%(class)s_changer")
    timestamp_change = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(blank=True)
    object_type = models.TextField(max_length=256, editable=False)
    object_id = models.IntegerField(editable=False)

    class Meta:
        abstract = True


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64, blank=True)  # TODO May be it should be unique???

    def __str__(self):
        return self.term_full

    class Meta:
        abstract = True


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

    syntactic_category_multi = models.ManyToManyField(SyntacticCategory)


class SourceType(Term):

    pass


class Source(Term):
    """Class representing sources of language information"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"
    description = models.TextField(blank=True)
    source_type = models.ForeignKey(SourceType)


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


class Dialect(Term):
    """Class represents dialect present in the system"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"
    parent_dialect = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])


class WritingSystemType(Term):
    """Class for constant writing system types list"""

    pass


class WritingSystem(Term):
    """Class represents a writing systems used to spell a word form"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"
    writing_system_type = models.ForeignKey(WritingSystemType)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.term_full


class LanguageEntity(models.Model):
    """Abstract base class used to tie an entity to a language"""

    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


class GrammCategorySet(LanguageEntity):
    """Class represents possible composite sets of grammar categories and its order in a given language
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    gramm_category_multi = models.ManyToManyField(GrammCategory)  # TODO: Fix string display due to this change
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
            return ' '.join(str(s) for s in self.gramm_category_multi.all())

    class Meta:
        unique_together = ('language', 'position')


class Inflection(LanguageEntity):

    syntactic_category_set = models.ForeignKey(SyntacticCategory)
    value = models.CharField(max_length=512)


class SemanticGroup(models.Model):
    theme = models.ManyToManyField(Theme, null=True, blank=True)


class Lexeme(LanguageEntity):
    """Class representing current lexemes
    """

    syntactic_category = models.ForeignKey(SyntacticCategory, null=True, blank=True)
    inflection = models.ForeignKey(Inflection, null=True, blank=True)
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


class RelationType(Term):
    """ Class for types of lexemes'  relations
    """
    pass


class LexemeRelation(models.Model):
    """ Class for lexemes' special relations
    """
    lexeme_1 = models.ForeignKey(Lexeme, related_name='relation_fst_set')
    lexeme_2 = models.ForeignKey(Lexeme, related_name='relation_snd_set')
    relation_type = models.ForeignKey(RelationType)


class DictEntity(models.Model):
    source = models.ManyToManyField(Source, null=True, blank=True)
    comment = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class WordformBase(DictEntity):
    """Base class for wordforms
    """

    lexeme = models.ForeignKey(Lexeme, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)
    spelling = models.CharField(max_length=512)
    writing_system = models.ForeignKey(WritingSystem)

    TRANSCRIPT_BRACKETS = {  # TODO Unhardcode this
        1: ('[{}]'),
        2: ('/{}/')
    }

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


class Translation(DictEntity):
    """Class representing current translations
    """

    lexeme_relation = models.ForeignKey(LexemeRelation, editable=False)
    direction = models.PositiveSmallIntegerField()
    semantic_group_1 = models.ForeignKey(SemanticGroup, null=True, blank=True, related_name='translation_fst_set')
    semantic_group_2 = models.ForeignKey(SemanticGroup, null=True, blank=True, related_name='translation_snd_set')
    usage_constraint_multi_1 = models.ManyToManyField(UsageConstraint, null=True, blank=True,
                                                      related_name='translation_fst_set')
    usage_constraint_multi_2 = models.ManyToManyField(UsageConstraint, null=True, blank=True,
                                                      related_name='translation_snd_set')
    dialect_multi_1 = models.ManyToManyField(Dialect, null=True, blank=True, related_name='translation_fst_set')
    dialect_multi_2 = models.ManyToManyField(Dialect, null=True, blank=True, related_name='translation_snd_set')
    comment_1 = models.TextField(blank=True)
    comment_2 = models.TextField(blank=True)
    translation_based = models.ManyToManyField('self', null=True, blank=True)
    is_visible = models.BooleanField()


# Dictionary classes


class TranslatedTerm(LanguageEntity):
    """Class representing term translation for the given language"""

    table = models.CharField(max_length=256)
    term_id = models.IntegerField()
    term_full_translation = models.CharField(max_length=256)
    term_abbr_translation = models.CharField(max_length=64, blank=True)


class Wordform(WordformBase):
    """Class representing current wordforms"""

    dialect_multi = models.ManyToManyField(Dialect, null=True, blank=True)

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


class WordformSample(WordformBase):
    """Class representing current wordform samples"""

    informant = models.CharField(max_length=256)


class WordformOrder:

    pass
