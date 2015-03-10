from django import forms
from django.db.models.loading import get_model
from django.forms.models import modelformset_factory, inlineformset_factory

from wordengine import models
from wordengine.global_const import *


class DoSmthWithIdForm(forms.Form):
    given_id = forms.IntegerField()


class WordformForm(forms.ModelForm):

    class Meta:
        model = models.Wordform
        widgets = {'dialect_multi': forms.CheckboxSelectMultiple}
        exclude = ['lexeme']


# class WordformSampleForm(forms.ModelForm):
#
#     class Meta:
#         model = models.WordformSample
#         exclude = ['lexeme']


class LexemeForm(forms.ModelForm):
    """Form representing fields of a lexeme class"""

    class Meta:
        model = models.Lexeme
        exclude = []


class SearchWordformForm(forms.Form):
    spelling = forms.CharField(required=False)
    language = forms.ModelChoiceField(queryset=models.Language.objects.all(), required=False)
    syntactic_category = forms.ModelChoiceField(queryset=models.SyntacticCategory.objects.all(), required=False)
    gramm_category = forms.ModelChoiceField(queryset=models.GrammCategorySet.objects.all(), required=False)
    source = forms.ModelChoiceField(queryset=models.Source.objects.all(), required=False)
    dialect = forms.ModelChoiceField(queryset=models.Dialect.objects.all(), required=False)


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


class ProjectUploadForm(UploadFileForm):
    source = forms.ModelChoiceField(queryset=models.Source.objects.all())


class ProjectListForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all())


class ProjectColumnSetupForm(forms.ModelForm):

    class Meta:
        model = models.ProjectColumn
        exclude = []
        widgets = {'project': forms.HiddenInput, 'state': forms.HiddenInput, 'language_l': forms.HiddenInput,
                   'dialect_l': forms.HiddenInput, 'writing_system_l': forms.HiddenInput,
                   'num': forms.HiddenInput, 'csvcell': forms.HiddenInput}

PrColSetupFormSet = inlineformset_factory(models.Project, models.ProjectColumn, ProjectColumnSetupForm, extra=0,
                                          can_delete=False)


class UntypedParamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UntypedParamForm, self).__init__(*args, **kwargs)
        model = get_model(APP_NAME, self.initial['src_obj'])
        params = model.project_fields()['params']
        available_terms = ((None, '---------'), )
        available_terms += tuple(((param, param) for param in params))
        self.fields['term_type'] = forms.ChoiceField(choices=available_terms, required=False)

    class Meta:
        model = models.ProjectDictionary
        exclude = ['state', 'project', 'term_id']
        widgets = {'value': forms.HiddenInput, 'src_obj': forms.HiddenInput}

UntypedParamFormSet = inlineformset_factory(models.Project, models.ProjectDictionary, form=UntypedParamForm, extra=0,
                                            can_delete=False)


class ParamSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParamSetupForm, self).__init__(*args, **kwargs)
        # if self.initial:
        choices = [(None, '---------')]
        for term in get_model(APP_NAME, self.initial['term_type']).objects.all():
                choices.append((term.id, term.__str__()), )
        self.fields['term_id'] = forms.ChoiceField(choices=choices, required=False)
    # It may be a good idea to cache choices at a formset level, so it is loaded only once per model

    # TODO Update state 'N' -> 'P' if valid (custom validation?)

    class Meta:
        model = models.ProjectDictionary
        exclude = ['project', 'src_field', 'src_obj']
        widgets = {'term_type': forms.HiddenInput, 'value': forms.HiddenInput, 'state': forms.HiddenInput}

ParamSetupFormSet = inlineformset_factory(models.Project, models.ProjectDictionary, form=ParamSetupForm, extra=0,
                                          can_delete=False)

