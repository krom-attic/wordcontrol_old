from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from wordengine import forms, models


def index(request):
    return render(request, 'wordengine/index.html')

def ActionResultView(request):
    return render(request, 'wordengine/action_result.html')


class DoSmthWordFormView(TemplateView):
    some_object_class = forms.DoSmthWithIdForm
    template_name = 'wordengine/do_smth.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'smth_form': self.some_object_class()})

    def post(self, request, *args, **kwargs):
        if '_delete_wordform' in request.POST:
            word_form = get_object_or_404(models.WordForm, pk=request.POST['given_id'])
            # if the corresponding lexeme doesn't have another wordforms:
                # if it has a translation, block wordform deletion
                # if it doesn't, delete the lexeme and the wordform, record the deletion
            # if the lexeme has another wordforms, delete a wordform, record the deletion
            word_form.is_deleted = True
            word_form.save()
        elif '_restore_wordform' in request.POST:
            word_form = get_object_or_404(models.WordForm, pk=request.POST['given_id'])
            word_form.is_deleted = False
            word_form.save()
        return redirect(reverse('wordengine:action_result'))


class AddWordFormView(TemplateView):
    word_form_class = forms.NewWordFormForm
    lexeme_form_class = forms.LexemeForm
    source_form_class = forms.SourceSelectForm
    template_name = 'wordengine/add_word.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'word_form': self.word_form_class(),
                                                    'lexeme_form': self.lexeme_form_class(),
                                                    'source_form': self.source_form_class()})

    def post(self, request, *args, **kwargs):
        is_saved = False
        lexeme_form = self.lexeme_form_class(request.POST)
        source_form = self.source_form_class(request.POST)
        if lexeme_form.is_valid() and source_form.is_valid():
            lexeme = lexeme_form.save()
            source = source_form.cleaned_data['source']
            change = models.DictChange(source=source, user_changer=request.user)
            change.save()
            word_form_initial = models.WordForm(lexeme=lexeme, dict_change_commit=change)
            word_form = self.word_form_class(request.POST, instance=word_form_initial)
            if word_form.is_valid():
                word_form.save()
                is_saved = True
        if not is_saved:
            return render(request, self.template_name, {'word_form': word_form, 'lexeme_form': lexeme_form,
                                                        'source_form': source_form})

        if '_continue_edit' in request.POST:
            return redirect(reverse('wordengine:index'))
        elif '_add_new' in request.POST:
            return redirect(reverse('wordengine:add_wordform'))
        else:
            return redirect(reverse('wordengine:index'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddWordFormView, self).dispatch(*args, **kwargs)


class ShowWordFormListView(TemplateView):
    word_search_class = forms.SearchWordFormForm
    template_name = 'wordengine/wordform_list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'word_search': self.word_search_class()})

    def post(self, request, *args, **kwargs):
        is_searched = True
        if 'given_string' in request.POST:
            word_result = models.WordForm.objects.filter(spelling__startswith=request.POST['given_string'])
        return render(request, self.template_name, {'word_search': self.word_search_class(),
                                                    'word_result': word_result, 'is_searched': is_searched})


class ShowLexemeDetailsView(TemplateView):
    template_name = 'wordengine/lexeme_details.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)