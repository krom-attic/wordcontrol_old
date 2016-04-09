from django.core.urlresolvers import reverse
from django.db import models
from lazy import lazy

from wordengine.dict_utils.formatter import EntryFormatter
from wordengine.lexeme_utils.parser import LexemeEnrtyParser
from wordengine.model.dictionary import Dictionary
from wordengine.model.language_entity import LanguageEntity
from wordengine.model.mixins import Timestampable
from wordengine.model.synt_cats_in_language import SyntCatsInLanguage
from wordengine.model.syntactic_category import SyntacticCategory


class LexemeEntry(LanguageEntity, Timestampable):
    """
    New style lexeme class
    """

    dictionary = models.ForeignKey(Dictionary)
    reverse_generated = models.BooleanField(editable=False, default=False)
    syntactic_category = models.ForeignKey(SyntacticCategory)
    forms_text = models.TextField()
    relations_text = models.TextField(blank=True)
    translations_text = models.TextField(blank=True)
    sources_text = models.TextField(blank=True)
    slug = models.SlugField(max_length=128)
    disambig = models.SmallIntegerField(null=True, blank=True)
    caption_form = models.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unsaved_wordform_spellings = []

    def __str__(self):
        return ' | '.join(str(s) for s in [self.caption_form,  self.language, self.syntactic_category])

    def get_absolute_url(self):
        if self.disambig:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug, 'disambig': self.disambig})
        else:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug})

    @lazy
    def view_url(self):
        return self.get_absolute_url()

    @lazy
    def edit_url(self):
        return reverse('wordengine:edit_lexeme_entry', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if kwargs.pop('explicit'):
            return super().save(*args, **kwargs)
        else:
            raise Exception('All lexeme entry saves must be made explicitly')

    @lazy
    def all_forms(self):
        """
        Returns a plain dictionary of wordforms, grouped by form
        :return: {form: (wordforms, ...), ...}
        """
        all_forms = {SyntCatsInLanguage.main_gr_cat_set(self.syntactic_category, self.language): self.mainform_full}
        all_forms.update(self.oblique_forms)
        return all_forms

    @lazy
    def forms(self):
        return LexemeEnrtyParser(self).split_forms()

    @lazy
    def mainform_full(self):
        return self.forms['main']

    @lazy
    def mainform_short(self):
        return self.mainform_full[0]

    @lazy
    def mainform_caption(self):
        return self.mainform_short['spellings'][0]

    @lazy
    def comment(self):
        return self.forms['comment']

    @lazy
    def oblique_forms(self):
        return self.forms['oblique']

    @lazy
    def relations(self):
        return LexemeEnrtyParser(self).split_relations()

    @lazy
    def translations(self):
        return LexemeEnrtyParser(self).split_translations()

    @lazy
    def sources(self):
        return LexemeEnrtyParser(self).split_sources()
