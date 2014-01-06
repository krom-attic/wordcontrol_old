from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from wordengine import forms
from wordengine import models


class AddWordFormView(TemplateView):
    word_form_class = forms.NewWordFormForm
    lexeme_form_class = forms.LexemeForm
    template_name = 'wordengine/add_word.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'word_form': self.word_form_class,
                                                    'lexeme_form': self.lexeme_form_class})

    def post(self, request, *args, kwargs):
        lexeme = self.lexeme_form_class(request.POST)
        lexeme.save()
        word_form_initial = models.WordForm(lexeme=lexeme)
        word_form = self.word_form_class(request.POST, instance=word_form_initial)
        word_form.save()
        if '_continue_edit' in request.POST:
            return redirect(reverse('wordengine:index'))
        elif '_add_new' in request.POST:
            return redirect(reverse('wordengine:add_wordform'))
        else:
            return redirect(reverse('wordengine:index'))

    @login_required
    def dispatch(self, *args, **kwargs):
        return super(AddWordFormView, self).dispatch(*args, **kwargs)