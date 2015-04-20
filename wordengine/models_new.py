# V2 Classes
import slugify
from lazy import lazy

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wordengine.global_const import *

# Global lists. Abstract


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField(max_length=256)
    term_abbr = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.term_full

    class Meta:
        abstract = True


# Global lists. Concrete


class SyntacticCategory(Term):
    """Class represents syntactic category (used in lexemes) list"""

    pass


class Language(Term):
    """Class represents languages present in the system"""

    syntactic_category_m = models.ManyToManyField(SyntacticCategory, through='SyntCatsInLanguage',
                                                  through_fields=('language', 'syntactic_category'),
                                                  blank=True, related_name='synt_cat_set')
    iso_code = models.CharField(max_length=8, db_index=True)  # ISO 639-3

    def get_main_gr_cat(self, synt_cat):
        return self.syntcatsinlanguage_set.get(syntactic_category=synt_cat).main_gramm_category_set


class GrammCategoryType(Term):
    """Class represents types of grammatical categories"""

    pass


class GrammCategory(Term):
    """Class represents values list for grammatical categories"""

    gramm_category_type = models.ForeignKey(GrammCategoryType)
    position = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return ' '.join([self.term_full, str(self.gramm_category_type)])


# Language-dependant classes. Abstract


class LanguageEntity(models.Model):
    """Abstract base class used to tie an entity to a language"""

    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


# Language-dependant classes. Concrete


class Dialect(Term, LanguageEntity):
    """Class represents dialect present in the system"""

    parent_dialect = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        unique_together = ('term_abbr', 'language')

    def __str__(self):
        return ' '.join([self.term_full, str(self.language)])


class WritingRelated(models.Model):
    writing_type = models.CharField(choices=WS_TYPE, max_length=2)

    class Meta:
        abstract = True


class WritingSystem(Term, WritingRelated):
    """Class represents a writing systems used to spell a word form"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"


class GrammCategorySet(LanguageEntity):
    """Class represents possible composite sets of grammar categories and its order in a given language
    """

    syntactic_category = models.ForeignKey(SyntacticCategory)
    gramm_category_m = models.ManyToManyField(GrammCategory)
    position = models.SmallIntegerField(null=True, blank=True)
    abbr_name = models.CharField(max_length=32, db_index=True)

    class Meta:
        unique_together = ('language', 'position')

    def __str__(self):
            return ' '.join(str(s) for s in self.gramm_category_m.all())

    @classmethod
    def get_gr_cat_set_by_abbr(cls, abbr):
        return cls.objects.get(abbr_name=abbr)


class SyntCatsInLanguage(models.Model):
    language = models.ForeignKey(Language)
    syntactic_category = models.ForeignKey(SyntacticCategory)
    main_gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True)

    def __str__(self):
        return ' '.join((str(self.language), str(self.syntactic_category) + ':', str(self.main_gramm_category_set)))

    @classmethod
    def is_in(cls, synt_cat, language):
        try:
            return cls.objects.get(language=language, syntactic_category=synt_cat)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def main_gr_cat_set(cls, synt_cat, language):
        try:
            return cls.objects.get(language=language, syntactic_category=synt_cat).main_gramm_category_set
        except ObjectDoesNotExist:
            return None


# Concrete dictionary classes


class Dictionary(models.Model):
    DICT_TYPES = (('U', 'User'), ('D', 'Digitized'), ('P', 'Public'))
    writing_systems = models.ManyToManyField(WritingSystem, through='WSInDict')
    type = models.CharField(choices=DICT_TYPES, max_length=1)
    maintainer = models.ForeignKey(User)
    caption = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return '{} dictionary "{}" by {}'.format(
            self.get_type_display(),
            self.caption or 'Unnamed dictionary',
            str(self.maintainer),
        )


class LexemeEnrtyParser():

    lexeme_entry = None

    def __init__(self, lexeme_entry):
        self.lexeme_entry = lexeme_entry

    # Helper splitters

    @staticmethod
    def get_dialect(dialect_abbr, language):
        try:
            dialect = Dialect.objects.get(term_abbr=dialect_abbr, language=language)
        except ObjectDoesNotExist:
            # TODO Raise an error
            dialect = dialect_abbr
        return dialect

    @staticmethod
    def get_language(lang_code):
        try:
            language = Language.objects.get(iso_code=lang_code)
        except ObjectDoesNotExist:
            # TODO Raise an error
            language = Language.objects.get(pk=1)
        return language

    def _split_wf(self, wf_literal):
        """
        Splits a string of wordforms, separated by comma.
        Then pops a dialect mark from the wordform.
        :param wf_literal: 'Wordform1=Wordform1_alt, Wordform2=Wordform2_alt <Dialect>, ..., WordformN'
        :return: [{'spellings': [Wordform1, Wordform1_alt], 'dialects': []}, {'spellings': [Wordform2, Wordform2_alt],
                  'dialects': [Dialect]}, {'spellings': [WordformN], 'dialects': []}]
        """

        wordforms = []

        for wordform in wf_literal.split(','):
            dialects = []
            wf_dialect = RE_DIALECT.split(wordform.strip())
            # TODO Check that the first element is not empty
            # TODO Check that there is nothing between dialects
            while len(wf_dialect) > 1:
                wf_dialect.pop()
                dialects.append(self.get_dialect(wf_dialect.pop().strip(), self.lexeme_entry.language))
            spellings = wf_dialect.pop().split('=')
            wordforms.append({'spellings': spellings, 'dialects': dialects})

        return wordforms

    @staticmethod
    def _split_transl_entry(transl_entry):
        examples = []
        pre_split = RE_EXAMPLE.split(transl_entry.strip())
        while len(pre_split) > 1:
            examples.append(pre_split.pop().strip())
            pre_split.pop()
        # TODO Check that the first element is not empty
        comm_split = RE_COMMENT_NEW.split(pre_split.pop().strip(), 1)
        if len(comm_split) > 1:
            # TODO Check that the last element is not empty
            comment = comm_split[1].strip()
        else:
            comment = ''
        word = comm_split[0].strip()
        if word[:2] == '$:':
            is_reverse = True
            word = word[2:].strip()
        else:
            is_reverse = False
        return {'word': word, 'comment': comment, 'examples': examples, 'is_reverse': is_reverse}

    def _split_semantic_groups(self, language_group, language):
        semanitc_groups = RE_SEM_GR.split(language_group)
        translation_entries = []
        # TODO Check that the first element is empty
        for semanitc_group in semanitc_groups[1:]:
            sem_gr_spl = RE_DIALECT.split(semanitc_group.strip())
            comm_transl = RE_GROUP_COMMENT.split(sem_gr_spl.pop().strip(), 1)
            translations = (self._split_transl_entry(translation)
                            for translation in comm_transl.pop().strip().split(';'))
            if len(comm_transl) > 1:
                comment = comm_transl.pop()
            else:
                comment = ''
            # TODO Check that the first element is empty
            dialects = []
            while len(sem_gr_spl) > 1:
                # TODO Check if there are only empty elements between dialect marks
                # TODO Add support to place comment in front of dialects list
                dialects.append(self.get_dialect(sem_gr_spl.pop().strip(), language))
                sem_gr_spl.pop()

            # TODO Add semantic group order
            translation_entries.append({'comment': comment, 'dialects': dialects,
                                        'translations': translations})
        return translation_entries

    # Main splitters

    def split_forms(self):
        """
        Splits a "forms" string into main form, oblique forms and word comment
        :return: {'main': split_wf(forms), 'comment': comment,
                  'oblique': {'formN': split_wf(forms), 'formM': split_wf(forms), ...}}
        """
        oblique_forms = {}
        comment = ''
        forms_text = self.lexeme_entry.forms_text.strip()
        forms_split = RE_FORM.split(forms_text)
        for i in range(1, len(forms_split), 2):
            oblique_forms[forms_split[i].strip()] = self._split_wf(forms_split[i+1].strip())
        # TODO Check that the first element is not empty
        main_comment = RE_COMMENT_NEW.split(forms_split[0].strip(), 1)

        if len(main_comment) == 3:
            # TODO Check that the last element is empty
            main_comment.pop()
            comment = main_comment.pop()
        main_form = self._split_wf(main_comment.pop())

        return {'main': main_form, 'comment': comment, 'oblique': oblique_forms}

    def split_relations(self):
        relations_text = self.lexeme_entry.relations_text.strip()
        if not relations_text:
            return {}
        relations = relations_text.split(':', 1)
        rel_dests = (rel.strip() for rel in relations.pop().split('+'))
        rel_type = RELATION_TYPES[relations.pop().lower()]
        return {rel_type: rel_dests}

    def split_translations(self):
        # TODO Check that the first element is empty
        translations_text = self.lexeme_entry.translations_text.strip()
        transl_spl = RE_TRANSL.split(translations_text)
        translations = {}
        for i in range(1, len(transl_spl), 2):
            language = self.get_language(transl_spl[i])
            # TODO Raise an error if
            transl_temp = translations.setdefault(language, [])
            translations[language] = transl_temp + self._split_semantic_groups(transl_spl[i+1], language)
        return translations

    def split_sources(self):
        sources_text = self.lexeme_entry.sources_text.strip()
        if not sources_text:
            return ()
        sources = (source.strip().split(':') for source in sources_text.split(';'))
        return ({'source': source[0].strip(), 'entry': source[1].strip()} for source in sources)


class LexemeEntry(LanguageEntity):
    """
    New style lexeme class
    """
    syntactic_category = models.ForeignKey(SyntacticCategory)
    forms_text = models.TextField()
    relations_text = models.TextField(blank=True)
    translations_text = models.TextField(blank=True)
    sources_text = models.TextField(blank=True)
    slug = models.SlugField(max_length=128)
    dictionary = models.ForeignKey(Dictionary)
    disambig = models.CharField(max_length=64, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Parser = LexemeEnrtyParser(self)

    def get_absolute_url(self):
        if self.disambig:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug, 'disambig': self.disambig})
        else:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug})

    def save(self, *args, **kwargs):
        if 'only_slug_update' in kwargs:
            kwargs.pop('only_slug_update')
            return super().save(*args, **kwargs)
        # Determine if the object is new or not
        if self.pk:
            # Get an original object
            old_entry = LexemeEntry.objects.get(pk=self.id)
            # print(old_entry)
            # Compare
            if not self == old_entry:
                pass
                # Update lookup field if needed
                # Check other links
        else:
            # Create wordform spellings for the entry
            pass
        self.slug = slugify.slugify(self.mainform_caption)

        # Check if disambiguation is needed and if it is, use plain numbering
        existant_entries = LexemeEntry.objects.filter(slug=self.slug)
        if existant_entries.count() == 1:
            existant_entry = existant_entries[0]
            existant_entry.disambig = '1'
            existant_entry.save(only_slug_update=True)
            self.disambig = '2'
        elif existant_entries.count() > 1:
            self.disambig = int(existant_entries.aggregate(models.Max('disambig'))['disambig__max']) + 1

        return super().save(*args, **kwargs)

    def __str__(self):
        return ' | '.join(str(s) for s in [self.mainform_caption,  self.language, self.syntactic_category])

    @lazy
    def all_forms(self):
        all_forms = {SyntCatsInLanguage.main_gr_cat_set(self.syntactic_category, self.language): self.mainform_full}
        all_forms.update(self.oblique_forms)
        return all_forms

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
    def forms(self):
        return self.Parser.split_forms()

    @lazy
    def relations(self):
        return self.Parser.split_relations()

    @lazy
    def translations(self):
        return self.Parser.split_translations()

    @lazy
    def sources(self):
        return self.Parser.split_sources()

    @lazy
    def wordform_spellings(self):
        wordform_objects = []
        wordforms = self.all_forms
        for form in wordforms:
            try:
                gramm_cat_set = GrammCategorySet.get_gr_cat_set_by_abbr(form)
            except ObjectDoesNotExist:
                # TODO Add an error to an errorlist
                pass
            for wordform in wordforms[form]:
                dialects = []
                for dialect in wordform:
                    try:
                        dialects.append(Dialect.objects.get(term_abbr=dialect, language=self.language))
                    except ObjectDoesNotExist:
                        # TODO Add an error to an errorlist
                        pass
                for spelling in wordform['spellings']:
                    wf_spell = WordformSpelling(spelling=spelling, writing_system=None,
                                                gramm_category_set=gramm_cat_set, lexeme_entry=self)
                    wf_spell.dialects.add(*dialects)
        # TODO Return a list of wordforms or an errorlist
        return wordform_objects

    @lazy
    def view_url(self):
        return self.get_absolute_url()

    @lazy
    def edit_url(self):
        return reverse('wordengine:edit_lexeme_entry', kwargs={'pk': self.pk})


class WordformSpelling(models.Model):
    lexeme_entry = models.ForeignKey(LexemeEntry, editable=False)
    spelling = models.CharField(max_length=512, editable=False)
    gramm_category_set = models.ForeignKey(GrammCategorySet, null=True, blank=True, editable=False)
    dialects = models.ManyToManyField(Dialect, blank=True, editable=False)
    comment = models.TextField(blank=True, editable=False)
    writing_system = models.ForeignKey(WritingSystem, editable=False)