from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from wordengine.model.language_entity import LanguageEntity
from wordengine.model.term import Term


class Dialect(Term, LanguageEntity):
    """Class represents dialect present in the system"""

    parent_dialect = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        unique_together = ('term_abbr', 'language')

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])

    @classmethod
    def get_dialect_by_abbr(cls, dialect_abbr, language):
        try:
            dialect = cls.objects.get(term_abbr__iexact=dialect_abbr, language=language)
        except ObjectDoesNotExist:
            # TODO Raise an error
            dialect = dialect_abbr
        return dialect