import django_filters
from wordengine import models


class LexemeEntryFilter(django_filters.FilterSet):
    class Meta:
        model = models.LexemeEntry
        fields = ['dictionary', 'wordformspelling__spelling', 'language', 'syntactic_category']