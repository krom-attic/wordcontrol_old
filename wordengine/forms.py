from django import forms
from wordengine import models


class WordFormForm(forms.ModelForm):

    class Meta:
        model = models.WordForm
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
        exclude = ['lexeme']


class LexemeForm(forms.ModelForm):
    """Form representing fields of a lexeme class"""

    class Meta:
        model = models.Lexeme


class SourceSelectForm(forms.Form):
    """Form representing fields of a lexeme class"""

    source = forms.ModelChoiceField(queryset=models.Source.objects.all())


class DoSmthWithIdForm(forms.Form):
    given_id = forms.IntegerField()


class SearchWordFormForm(forms.Form):
    spelling = forms.CharField(required=False)
    language = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    syntactic_category = forms.ModelChoiceField(queryset=models.SyntacticCategory.objects.all(), required=False)
