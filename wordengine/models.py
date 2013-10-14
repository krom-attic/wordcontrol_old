from django.db import models
from django.contrib import auth

# Global abstract classes


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(auth.models.User, editable=False, related_name="%(app_label)s_%(class)s_changer")
    timestamp_change = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField()

    class Meta:
        abstract = True


class Source(models.Model):
    """Class representing sources of language information"""


    name = models.CharField(max_length=256)


class DictChange(Change):
    """This class extends Change class with fields representing change review and information source for
     WordForms and Translations"""


    user_reviewer = models.ForeignKey(auth.models.User, editable=False, null=True)
    timestamp_review = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    source = models.ForeignKey(Source)


class MiscChange(Change):
    """This class extends Change class with fields representing generic change"""


    table_name = models.CharField(max_length=256)
    field_name = models.CharField(max_length=256)
    old_value = models.CharField(max_length=512)
    new_value = models.CharField(max_length=512)


# Dictionary term models


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64)

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


class GrammarCategorySet(models.Model):
    """Class represents possible composite sets of grammar categories in a given language"""


    animacy = models.ForeignKey(Animacy, null=True)
    aspect = models.ForeignKey(Aspect, null=True)
    case = models.ForeignKey(Case, null=True)
    comparison = models.ForeignKey(Comparison, null=True)
    gender = models.ForeignKey(Gender, null=True)
    mood = models.ForeignKey(Mood, null=True)
    number = models.ForeignKey(Number, null=True)
    person = models.ForeignKey(Person, null=True)
    polarity = models.ForeignKey(Polarity, null=True)
    tense = models.ForeignKey(Tense, null=True)
    voice = models.ForeignKey(Voice, null=True)


class Language(Term):
    """Class represents languages present in the system"""


    syntactic_categories = models.ManyToManyField(SyntacticCategory)
    grammar_category_sets = models.ManyToManyField(GrammarCategorySet)


class Dialect(Term):
    """Class represents dialect present in the system"""


    language = models.ForeignKey(Language)
    parent_dialect = models.ForeignKey('self', null=True)


class WritingSystem(Term):
    """Class represents a writing systems used to spell a word form"""


    language = models.ForeignKey(Language)  #Null means "language independent"
    description = models.TextField()


class LanguageEntity(models.Model):
    """Abstract base class used to tie an entity to a language"""


    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


class LexemeBase(LanguageEntity):
    """Base class for current lexemes"""


    syntactic_category = models.ForeignKey(SyntacticCategory)

    class Meta:
        abstract = True


class Lexeme(LexemeBase):
    pass


class LexemeDeleted(LexemeBase):
    lexeme = models.ForeignKey(Lexeme)


class WordFormBase(LanguageEntity):
    lexeme = models.ForeignKey(Lexeme)
    dialects = models.ManyToManyField(Dialect)
    grammar_category_set = models.ForeignKey(GrammarCategorySet)
    spelling = models.CharField(max_length=512)
    writing_system = models.ForeignKey(WritingSystem)
    dict_change_commit = models.ForeignKey(DictChange, editable=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class WordForm(WordFormBase):
    pass


class WordFormPrevious(WordFormBase):
    word_form = models.ForeignKey(WordForm)
    dict_change_replace = models.ForeignKey(DictChange, related_name='replace_word_form _set')


class WordFormDeleted(WordFormBase):
    word_form = models.ForeignKey(WordForm)
    dict_change_delete = models.ForeignKey(DictChange, related_name='delete_word_form _set')
    dict_change_restore = models.ForeignKey(DictChange, related_name='restore_word_form_set')


class TranslationBase(models.Model):
    lexeme_1 = models.ForeignKey(Lexeme, related_name='translationbase_fst_set')
    lexeme_2 = models.ForeignKey(Lexeme, related_name='translationbase_snd_set')
    usage_constraint = models.ForeignKey(UsageConstraint)
    comment = models.TextField(null=True)
    dict_change_commit = models.ForeignKey(DictChange)
    is_deleted = models.BooleanField(default=False)


class Translation(TranslationBase):
    pass


class TranslationDeleted(TranslationBase):
    translation = models.ForeignKey(Translation)
    dict_change_delete = models.ForeignKey(DictChange, related_name='delete_translation_set')
    dict_change_restore = models.ForeignKey(DictChange, related_name='restore_translation_set')


class TranslatedTerm(LanguageEntity):
    table = models.CharField(max_length=256)
    term_id = models.IntegerField()
    term_full_translation = models.CharField(max_length=256)
    term_abbr_translation = models.CharField(max_length=64)


