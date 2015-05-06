import django_filters
from wordengine import models


class LexemeEntryFilter(django_filters.FilterSet):
    wordformspelling__spelling = django_filters.CharFilter(lookup_type=('icontains', 'iexact'), label='Spelling')
    dictionary = django_filters.ModelMultipleChoiceFilter(queryset=models.Dictionary.objects.all())

    class Meta:
        model = models.LexemeEntry
        fields = ['dictionary', 'wordformspelling__spelling', 'language', 'syntactic_category']