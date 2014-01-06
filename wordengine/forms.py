from django import forms
from wordengine import models


class NewWordFormForm(forms.ModelForm):
    class Meta:
        model = models.WordForm
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
        exclude = ['lexeme']


class LexemeForm(forms.ModelForm):
    class Meta:
        model = models.Lexeme


class WordFormForm(forms.ModelForm):
    class Meta:
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
