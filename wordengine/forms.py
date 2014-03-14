from django import forms
from wordengine import models


class WordformForm(forms.ModelForm):

    class Meta:
        model = models.Wordform
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
        exclude = ['lexeme']


class LexemeForm(forms.ModelForm):
    """Form representing fields of a lexeme class"""

    class Meta:
        model = models.Lexeme
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}


class SourceSelectForm(forms.Form):
    """Form representing fields of a lexeme class"""

    source = forms.ModelChoiceField(queryset=models.Source.objects.all(), required=False)


class DoSmthWithIdForm(forms.Form):
    given_id = forms.IntegerField()


class SearchWordformForm(forms.Form):
    spelling = forms.CharField(required=False)
    language = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    syntactic_category = forms.ModelChoiceField(queryset=models.SyntacticCategory.objects.all(), required=False)


class AddTranslationForm(forms.ModelForm):
    """Form representing translation
    """

    class Meta:
        model = models.Translation
        exclude = ['lexeme_1', 'lexeme_2']