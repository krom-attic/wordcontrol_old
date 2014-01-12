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


class SourceSelectForm(forms.Form):
    source = forms.ModelChoiceField(queryset=models.Source.objects.all())


class DoSmthWithIdForm(forms.Form):
    given_id = forms.IntegerField()
    object_type = forms.ChoiceField([('WordForm', 'WordForm')])