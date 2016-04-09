from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from wordengine.model.gramm_category_set import GrammCategorySet
from wordengine.model.language import Language
from wordengine.model.syntactic_category import SyntacticCategory


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
