from django.db import models

from wordengine.model.gramm_category_type import GrammCategoryType
from wordengine.model.term import Term

class GrammCategory(Term):
    """Class represents values list for grammatical categories"""

    gramm_category_type = models.ForeignKey(GrammCategoryType)
    position = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['gramm_category_type', 'position']

    def __str__(self):
        return ' '.join([self.term_full, str(self.gramm_category_type)])
