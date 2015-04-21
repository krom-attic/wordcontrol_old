from wordengine.models_global import *
from wordengine.global_const import *

from django.core.exceptions import ObjectDoesNotExist

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

    class Meta:
        unique_together = ('term_abbr', 'language')

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])


class WritingRelated(models.Model):
    writing_type = models.CharField(choices=WS_TYPE, max_length=2)

    class Meta:
        abstract = True


class WritingSystem(Term, WritingRelated):
    """Class represents a writing systems used to spell a word form"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"


class GrammCategorySet(LanguageEntity):
    """Class represents possible composite sets of grammar categories and its order in a given language
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    gramm_category_m = models.ManyToManyField(GrammCategory)
    position = models.SmallIntegerField(null=True, blank=True)
    abbr_name = models.CharField(max_length=32, db_index=True)

    class Meta:
        unique_together = (('language', 'position'), ('language', 'abbr_name'))

    def __str__(self):
            return ' '.join(str(s) for s in self.gramm_category_m.all())


class SyntCatsInLanguage(models.Model):
    language = models.ForeignKey(Language)
    syntactic_category = models.ForeignKey(SyntacticCategory)
    main_gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)

    def __str__(self):
        return ' '.join((str(self.language), str(self.syntactic_category) + ':', str(self.main_gramm_category_set)))

    @classmethod
    def is_in(cls, synt_cat, language):
        try:
            return cls.objects.get(language=language, syntactic_category=synt_cat)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def main_gr_cat_set(cls, synt_cat, language):
        try:
            return cls.objects.get(language=language, syntactic_category=synt_cat).main_gramm_category_set
        except ObjectDoesNotExist:
            return None