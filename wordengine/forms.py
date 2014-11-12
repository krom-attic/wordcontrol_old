from django import forms
from wordengine import models
from wordengine.global_const import *


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
        exclude = []



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


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ProjectListForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all())


class ProjectColumnSetupForm(forms.ModelForm):

    class Meta:
        model = models.ProjectColumn
        exclude = []
        widgets = {'project': forms.HiddenInput, 'state': forms.HiddenInput, 'language_l': forms.HiddenInput,
                   'dialect_l': forms.HiddenInput, 'source_l': forms.HiddenInput, 'writing_system_l': forms.HiddenInput,
                   'processing_l': forms.HiddenInput, 'num': forms.HiddenInput, 'csvcell': forms.HiddenInput}


class ProjectDictionaryForm(forms.Form):
    pass


class UntypedParamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UntypedParamForm, self).__init__(*args, **kwargs)
        self.fields['term_type'] = forms.ChoiceField(choices=TERM_TYPES[(self.initial['src_obj'],
                                                                         self.initial['src_field'])])

    class Meta:
        model = models.ProjectDictionary
        exclude = ['term_id', 'state', 'project']
        widgets = {'value': forms.HiddenInput, 'src_field': forms.HiddenInput, 'src_obj': forms.HiddenInput}