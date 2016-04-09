from django.db import models
from wordengine.global_const import WS_TYPE


class WritingRelated(models.Model):
    writing_type = models.CharField(choices=WS_TYPE, max_length=2)

    class Meta:
        abstract = True

