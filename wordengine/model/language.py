from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from wordengine.model.syntactic_category import SyntacticCategory
from wordengine.model.term import Term


class Language(Term):
    """Class represents languages present in the system"""

    syntactic_category_m = models.ManyToManyField(SyntacticCategory, through='SyntCatsInLanguage',
                                                  through_fields=('language', 'syntactic_category'),
                                                  blank=True, related_name='synt_cat_set')
    iso_code = models.CharField(max_length=8, db_index=True)

    def get_main_gr_cat(self, synt_cat):
        return self.syntcatsinlanguage_set.get(syntactic_category=synt_cat).main_gramm_category_set

    @classmethod
    def get_language_by_code(cls, lang_code):
        try:
            language = cls.objects.get(iso_code=lang_code)
        except ObjectDoesNotExist:
            # TODO Raise an error
            language = cls.objects.get(pk=1)
        return language

