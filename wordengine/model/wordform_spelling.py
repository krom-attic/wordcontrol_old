from django.db import models
from wordengine.model.dialect import Dialect
from wordengine.model.gramm_category_set import GrammCategorySet
from wordengine.model.lexeme_entry import LexemeEntry
from wordengine.model.writing_system import WritingSystem


class WordformSpelling(models.Model):

    lexeme_entry = models.ForeignKey(LexemeEntry, editable=False)
    spelling = models.CharField(max_length=512, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True, editable=False)
    dialects = models.ManyToManyField(Dialect, blank=True, editable=False)
    writing_system = models.ForeignKey(WritingSystem, editable=False)

    def __str__(self):
        return 'Entry {}. {} : {}, ({})'.format(self.lexeme_entry, self.spelling, self.gramm_category_set,
                                                   self.writing_system)
        # TODO How to output Many-to-Many?
                                                   # ', '.join(self.dialects), self.writing_system)
