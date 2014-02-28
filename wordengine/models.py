from django.db import models
from django.contrib import auth

# Verified against Architecture Design as of 2013.12.30


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(auth.models.User, editable=False, related_name="%(app_label)s_%(class)s_changer")
    timestamp_change = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(blank=True)

    class Meta:
        abstract = True


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64, blank=True)

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


class Animacy(Term):
    """Class represents values list for Animacy grammatical category"""

    pass


class Aspect(Term):
    """Class represents values list for Aspect grammatical category"""

    pass


class Case(Term):
    """Class represents values list for Case grammatical category"""

    pass


class Comparison(Term):
    """Class represents values list for Comparison grammatical category"""

    pass


class Gender(Term):
    """Class represents values list for Gender grammatical category"""

    pass


class Mood(Term):
    """Class represents values list for Mood grammatical category"""

    pass


class Number(Term):
    """Class represents values list for Number grammatical category"""

    pass


class Person(Term):
    """Class represents values list for Person grammatical category"""

    pass


class Polarity(Term):
    """Class represents values list for Polarity grammatical category"""

    pass


class Tense(Term):
    """Class represents values list for Tense grammatical category"""

    pass


class Voice(Term):
    """Class represents values list for Voice grammatical category"""

    pass


class GrammCategorySet(models.Model):
    """Class represents possible composite sets of grammar categories in a given language"""

    syntactic_category = models.ForeignKey(SyntacticCategory)
    animacy = models.ForeignKey(Animacy, null=True, blank=True)
    aspect = models.ForeignKey(Aspect, null=True, blank=True)
    case = models.ForeignKey(Case, null=True, blank=True)
    comparison = models.ForeignKey(Comparison, null=True, blank=True)
    gender = models.ForeignKey(Gender, null=True, blank=True)
    mood = models.ForeignKey(Mood, null=True, blank=True)
    number = models.ForeignKey(Number, null=True, blank=True)
    person = models.ForeignKey(Person, null=True, blank=True)
    polarity = models.ForeignKey(Polarity, null=True, blank=True)
    tense = models.ForeignKey(Tense, null=True, blank=True)
    voice = models.ForeignKey(Voice, null=True, blank=True)

    def __str__(self):
            return ' '.join(str(s) for s in [self.syntactic_category, self.person, self.tense, self.case, self.aspect,
                                             self.voice, self.comparison, self.polarity, self.mood, self.animacy,
                                             self.gender, self.number]
                            if s)


class Language(Term):
    """Class represents languages present in the system"""

    syntactic_category_multi = models.ManyToManyField(SyntacticCategory)
    gramm_category_set_multi = models.ManyToManyField(GrammCategorySet)


class Source(Term):
    """Class representing sources of language information"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"
    description = models.TextField(blank=True)


class DictChange(Change):
    """This class extends Change class with fields representing change review and information source for
     WordForms and Translations"""

    user_reviewer = models.ForeignKey(auth.models.User, editable=False, null=True, blank=True)
    timestamp_review = models.DateTimeField(editable=False, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)


class MiscChange(Change):
    """This class extends Change class with fields representing generic change"""

    table_name = models.CharField(max_length=256)
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


class AnimacyLanguageOrder(LanguageEntity):
    """Class represents order of an Animacy grammatical category values in a language"""

    animacy = models.ForeignKey(Animacy)
    position = models.SmallIntegerField()


class AspectLanguageOrder(LanguageEntity):
    """Class represents order of an Aspect grammatical category values in a language"""

    aspect = models.ForeignKey(Aspect)
    position = models.SmallIntegerField()


class CaseLanguageOrder(LanguageEntity):
    """Class represents order of an Case grammatical category values in a language"""

    case = models.ForeignKey(Case)
    position = models.SmallIntegerField()


class ComparisonLanguageOrder(LanguageEntity):
    """Class represents order of an Comparison grammatical category values in a language"""

    comparison = models.ForeignKey(Comparison)
    position = models.SmallIntegerField()


class GenderLanguageOrder(LanguageEntity):
    """Class represents order of an Gender grammatical category values in a language"""

    gender = models.ForeignKey(Gender)
    position = models.SmallIntegerField()


class MoodLanguageOrder(LanguageEntity):
    """Class represents order of an Mood grammatical category values in a language"""

    mood = models.ForeignKey(Mood)
    position = models.SmallIntegerField()


class NumberLanguageOrder(LanguageEntity):
    """Class represents order of an Number grammatical category values in a language"""

    number = models.ForeignKey(Number)
    position = models.SmallIntegerField()


class PersonLanguageOrder(LanguageEntity):
    """Class represents order of an Person grammatical category values in a language"""

    person = models.ForeignKey(Person)
    position = models.SmallIntegerField()


class PolarityLanguageOrder(LanguageEntity):
    """Class represents order of an Polarity grammatical category values in a language"""

    polarity = models.ForeignKey(Polarity)
    position = models.SmallIntegerField()


class TenseLanguageOrder(LanguageEntity):
    """Class represents order of an Tense grammatical category values in a language"""

    tense = models.ForeignKey(Tense)
    position = models.SmallIntegerField()


class VoiceLanguageOrder(LanguageEntity):
    """Class represents order of an Voice grammatical category values in a language"""

    voice = models.ForeignKey(Voice)
    position = models.SmallIntegerField()


class GrammCategorySetLanguageOrder(LanguageEntity):

    gramm_category_set = models.ForeignKey(GrammCategorySet)
    position = models.SmallIntegerField()


class Inflection(LanguageEntity):

    syntactic_categort_set = models.ForeignKey(SyntacticCategory)
    value = models.CharField(max_length=512)


class LexemeBase(LanguageEntity):
    """Base class for lexemes"""

    syntactic_category = models.ForeignKey(SyntacticCategory, null=True, blank=True)
    dialect_multi = models.ManyToManyField(Dialect, null=True, blank=True)
    inflection = models.ForeignKey(Inflection, null=True, blank=True)

    class Meta:
        abstract = True


class Lexeme(LexemeBase):
    """Class representing current lexemes"""

    def __str__(self):
        return ' | '.join(str(s) for s in [self.wordform_set.first().spelling, self.language, self.syntactic_category])


class WordFormBase(models.Model):
    """Base class for wordforms"""

    lexeme = models.ForeignKey(Lexeme, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)
    spelling = models.CharField(max_length=512)
    writing_system = models.ForeignKey(WritingSystem, blank=True, null=True)
    dict_change_commit = models.ForeignKey(DictChange, editable=False)
    dialect_multi = models.ManyToManyField(Dialect, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    def __str__(self):
        if self.writing_system:
            ws = str(self.writing_system.term_abbr)
        else:
            ws = ""
        return '{0} ({1} {2}) | {3}'.format(self.spelling, str(self.lexeme.language), str(self.gramm_category_set), ws)
    #TODO Include dialects into description

    class Meta:
        abstract = True


class TranslationBase(models.Model):
    """Base class for translations"""

    lexeme_1 = models.ForeignKey(Lexeme, editable=False, related_name='translationbase_fst_set')
    lexeme_2 = models.ForeignKey(Lexeme, editable=False, related_name='translationbase_snd_set')
    usage_constraint = models.ForeignKey(UsageConstraint, null=True, blank=True)
    comment = models.TextField(blank=True)
    dict_change_commit = models.ForeignKey(DictChange, editable=False)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

# Dictionary classes


class TranslatedTerm(LanguageEntity):
    """Class representing term translation for the given language"""

    table = models.CharField(max_length=256)
    term_id = models.IntegerField()
    term_full_translation = models.CharField(max_length=256)
    term_abbr_translation = models.CharField(max_length=64, blank=True)


class Translation(TranslationBase):
    """Class representing current translations"""

    pass


class TranslationDeleted(models.Model):
    """Class representing translation deletions"""

    translation = models.ForeignKey(Translation)
    dict_change_delete = models.ForeignKey(DictChange, related_name='delete_translation_set')
    dict_change_restore = models.ForeignKey(DictChange, related_name='restore_translation_set', null=True, blank=True)


class WordForm(WordFormBase):
    """Class representing current wordforms"""

    pass


class WordFormPrevious(WordFormBase):
    """Class representing wordform replaces"""

    wordform = models.ForeignKey(WordForm)
    dict_change_replace = models.ForeignKey(DictChange, related_name='replace_wordform_set')


class WordFormDeleted(models.Model):
    """Class representing wordform deletions"""

    wordform = models.ForeignKey(WordForm)
    dict_change_delete = models.ForeignKey(DictChange, related_name='delete_wordform_set')
    dict_change_restore = models.ForeignKey(DictChange, related_name='restore_wordform_set', null=True, blank=True)