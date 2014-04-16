from django import forms
from wordengine import models


class DoSmthWithIdForm(forms.Form):
    given_id = forms.IntegerField()


class WordformForm(forms.ModelForm):

    class Meta:
        model = models.Wordform
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
        exclude = ['lexeme']


class WordformSampleForm(forms.ModelForm):

    class Meta:
        model = models.WordformSample
        exclude = ['lexeme']


class LexemeForm(forms.ModelForm):
    """Form representing fields of a lexeme class"""

    class Meta:
        model = models.Lexeme



class SearchWordformForm(forms.Form):
    spelling = forms.CharField(required=False)
    language = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    syntactic_category = forms.ModelChoiceField(queryset=models.SyntacticCategory.objects.all(), required=False)
    # Advanced search (filtering with dialect or grammatical category set) is possible


class AdminForm(forms.Form):
    """Form for admin panel"""

    language = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)


class AddTranslationForm(forms.ModelForm):
    """Form representing translation"""

    class Meta:
        model = models.Translation
        exclude = ['lexeme_1', 'lexeme_2']


class LanguageSetupForm(forms.ModelForm):
    """Form representing language settings"""

    class Meta:
        model = models.Language


class GrammCategorySetLanguageOrderForm(forms.ModelForm):
    """ Form for displaying grammar category sets and their application
    """

    class Meta:
        model = models.GrammCategorySetLanguageOrder
        widgets = {'gramm_category_set': forms.Select}
        exclude = ['language']

