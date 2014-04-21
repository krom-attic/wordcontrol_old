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


class GrammCategorySetForm(forms.ModelForm):
    """ Form for editing grammatical categories
    """

    class Meta:
        model = models.GrammCategorySet
        exclude = ['language']


class TranslationImportForm(forms.Form):
    """ Form for setting up initial parameters for quick translation addition
    """

    WORD_SOURCE_CHOICES = (
        (0, 'Not needed'),
        (1, 'As for translation'),
    )

    language_1 = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    language_2 = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    source_translation = forms.ModelChoiceField(queryset=models.Source.objects.all(), required=False)
    source_1 = forms.ChoiceField(choices=WORD_SOURCE_CHOICES, required=False)
    source_2 = forms.ChoiceField(choices=WORD_SOURCE_CHOICES, required=False)
    dialect_1_default = forms.ModelChoiceField(queryset=models.Dialect.objects.all(), required=False)
    dialect_2_default = forms.ModelChoiceField(queryset=models.Dialect.objects.all(), required=False)
    writing_system_ortho_1 = forms.ModelChoiceField(queryset=models.WritingSystem.objects.all(), required=False)
    writing_system_phon_1 = forms.ModelChoiceField(queryset=models.WritingSystem.objects.all(), required=False)
    writing_system_ortho_2 = forms.ModelChoiceField(queryset=models.WritingSystem.objects.all(), required=False)
    writing_system_phon_2 = forms.ModelChoiceField(queryset=models.WritingSystem.objects.all(), required=False)


class UploadFileForm(forms.Form):
    file  = forms.FileField()