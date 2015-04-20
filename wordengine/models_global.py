from django.db import models

# Global lists. Abstract


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.term_full

    class Meta:
        abstract = True


# Global lists. Concrete


class SyntacticCategory(Term):
    """Class represents syntactic category (used in lexemes) list"""

    pass


class Language(Term):
    """Class represents languages present in the system"""

    syntactic_category_m = models.ManyToManyField(SyntacticCategory, through='SyntCatsInLanguage',
                                                  through_fields=('language', 'syntactic_category'),
                                                  blank=True, related_name='synt_cat_set')
    iso_code = models.CharField(max_length=8, db_index=True)  # ISO 639-3

    def get_main_gr_cat(self, synt_cat):
        return self.syntcatsinlanguage_set.get(syntactic_category=synt_cat).main_gramm_category_set


class GrammCategoryType(Term):
    """Class represents types of grammatical categories"""

    pass


class GrammCategory(Term):
    """Class represents values list for grammatical categories"""

    gramm_category_type = models.ForeignKey(GrammCategoryType)
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.gramm_category_type)])