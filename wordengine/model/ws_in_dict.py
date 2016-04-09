from django.db import models
from wordengine.model.dictionary import Dictionary
from wordengine.model.language import Language
from wordengine.model.writing_system import WritingSystem


class WSInDict(models.Model):

    writing_system = models.ForeignKey(WritingSystem)
    dictionary = models.ForeignKey(Dictionary)
    language = models.ForeignKey(Language)
    order = models.SmallIntegerField()

    class Meta:
        unique_together = (('dictionary', 'order', 'language'), ('dictionary', 'writing_system', 'language'))
        ordering = ('language', 'order')

    def __str__(self):
        return '(dict #{}) {} [{}] {}'.format(self.dictionary.id, self.language, self.order, self.writing_system)
