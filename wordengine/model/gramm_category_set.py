from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from wordengine.model.gramm_category import GrammCategory
from wordengine.model.language_entity import LanguageEntity
from wordengine.model.syntactic_category import SyntacticCategory


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

    @classmethod
    def get_form_by_abbr(cls, form_abbr, language):
        try:
            form = cls.objects.get(abbr_name__iexact=form_abbr, language=language)
        except ObjectDoesNotExist:
            # TODO Raise an error
            form = form_abbr
        return form
