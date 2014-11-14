from django import forms
from wordengine import models
from wordengine.global_const import *
from django.db.models.loading import get_model
from django.db.models import Q


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


class UntypedParamForm(forms.ModelForm):
    term = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(UntypedParamForm, self).__init__(*args, **kwargs)

            # = forms.ChoiceField(choices=(('a', 'a'), ))
        # print(vars(self.fields['term']))
        # self.fields['content_type']._queryset
        # self.fields['content_type']._queryset
        # print(vars(self.fields['content_type']))
        # print(TERM_TYPES[(self.initial['src_obj'], self.initial['src_field'])])
        # TODO Here will be "ValueError: need more than 1 value to unpack" if non-tuple param leaks in
        available_terms = [kv[0] for kv in TERM_TYPES[(self.initial['src_obj'], self.initial['src_field'])]]
        self.fields['content_type'].queryset = models.ContentType.objects.filter(name__in=available_terms)
        # self.fields['term_type'] = forms.ChoiceField(choices=TERM_TYPES[(self.initial['src_obj'], self.initial['src_field'])])

    class Meta:
        model = models.ProjectDictionary
        exclude = ['term_id', 'state', 'project', 'object_id']
        widgets = {'value': forms.HiddenInput, 'src_field': forms.HiddenInput, 'src_obj': forms.HiddenInput}


class ParamSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParamSetupForm, self).__init__(*args, **kwargs)
        if self.initial:
            choices = []
            for term in get_model('wordengine', self.initial['term_type']).objects.all():
                choices.append((term.id, term.__str__()), )
            self.fields['term_id'] = forms.ChoiceField(choices=choices)
    # It may be a good idea to cache choices at a formset level, so it is loaded only once per model

    # TODO Update state 'N' -> 'P' if valid (custom validation?)

    class Meta:
        model = models.ProjectDictionary
        exclude = ['project', 'src_field', 'src_obj']
        widgets = {'term_type': forms.HiddenInput, 'value': forms.HiddenInput, 'state': forms.HiddenInput}
