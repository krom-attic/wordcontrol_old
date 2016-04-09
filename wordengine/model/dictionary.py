from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from wordengine.model.writing_system import WritingSystem


class Dictionary(models.Model):

    DICT_TYPES = (('U', 'User'), ('D', 'Digitized'), ('P', 'Public'))
    writing_systems = models.ManyToManyField(WritingSystem, through='WSInDict')
    type = models.CharField(choices=DICT_TYPES, max_length=1, default='U')
    maintainer = models.ForeignKey(User)
    caption = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return '{} dictionary "{}" by {}'.format(
            self.get_type_display(),
            self.caption or 'Unnamed dictionary',
            str(self.maintainer),
        )

    # TODO move away this method
    def get_ws(self, pos, language):
        return self.wsindict_set.get(order=pos, language=language).writing_system

    def get_ws_list(self):
        return self.wsindict_set.all()

    def ws_types_list(self, ws_type, language):
        return self.writing_systems.filter(writing_type=ws_type, language=language).values_list("writing_type")

    def get_absolute_url(self):
        return reverse('wordengine:view_dictionary', kwargs={'pk': self.pk})
