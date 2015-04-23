from wordengine.models_language import *

from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import User

import slugify
from lazy import lazy

RE_DIALECT = re.compile(r'<(.*?)>')
RE_FORM = re.compile(r'\{(.*?)\}')
RE_COMMENT = re.compile(r'"""(.*?)"""')
RE_GROUP_COMMENT = re.compile(r'^"""(.*?)"""')
RE_SEM_GR = re.compile(r'^[\d\*]\.', re.M)
RE_TRANSL = re.compile(r'^{(.*?)}', re.M)
RE_EXAMPLE = re.compile(r'>>(.*?)', re.M)
RE_DISAMBIG = re.compile(r'\((.*?)\)')

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

    def get_ws(self, pos):
        return WSInDict.objects.get(dictionary=self, order=pos).writing_system


class WSInDict(models.Model):
    writing_system = models.ForeignKey(WritingSystem)
    dictionary = models.ForeignKey(Dictionary)
    order = models.SmallIntegerField()

    class Meta:
        unique_together = ('dictionary', 'order')


class LexemeEnrtyParser():

    lexeme_entry = None

    def __init__(self, lexeme_entry):
        self.lexeme_entry = lexeme_entry

    # Helper splitters

    @staticmethod
    def get_dialect(dialect_abbr, language):
        try:
            dialect = Dialect.objects.get(term_abbr__iexact=dialect_abbr, language=language)
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

    @staticmethod
    def get_form(form_abbr, language):
        try:
            form = GrammCategorySet.objects.get(abbr_name__iexact=form_abbr, language=language)
        except ObjectDoesNotExist:
            form = form_abbr
        return form

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
        """

        :param transl_entry: $:translation (1) "" "Comment" "" \r\n >> Example
        :return: {'word': word, 'disambig': disambig, 'comment': comment, 'examples': examples,
                  'is_reverse': is_reverse}
        """
        examples = []
        pre_split = RE_EXAMPLE.split(transl_entry.strip())
        while len(pre_split) > 1:
            examples.append(pre_split.pop().strip())
            pre_split.pop()
        # TODO Check that the first element is not empty
        comm_split = RE_COMMENT.split(pre_split.pop().strip(), 1)
        if len(comm_split) > 1:
            # TODO Check that the last element is not empty
            comment = comm_split[1].strip()
        else:
            comment = ''
        word_split = RE_DISAMBIG.split(comm_split[0].strip(), 1)
        if len(word_split) > 1:
            # TODO Check that the last element is not empty
            disambig = word_split[1].strip()
        else:
            disambig = ''
        if word_split[0][:2] == '$:':
            is_reverse = True
            word = word_split[0][2:].strip()
        else:
            is_reverse = False
            word = word_split[0].strip()
        return {'word': word, 'disambig': disambig, 'comment': comment, 'examples': examples, 'is_reverse': is_reverse}

    def _split_semantic_groups(self, language_group, language):
        """

        :param language_group:
        :param language:
        :return: [{'comment': comment, 'dialects': dialects, 'translations': translations}, ...]
        """
        semanitc_groups = RE_SEM_GR.split(language_group)
        translation_entries = []
        if len(semanitc_groups) == 1:
            start = 0
        else:
            start = 1
            # First element must be empty
        for semanitc_group in semanitc_groups[start:]:
            sem_gr_spl = RE_DIALECT.split(semanitc_group.strip())
            comm_transl = RE_GROUP_COMMENT.split(sem_gr_spl.pop().strip(), 1)
            translations = tuple(self._split_transl_entry(translation)
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

            translation_entries.append({'comment': comment, 'dialects': dialects,
                                        'translations': translations})
            # TODO Add semantic group order
        return translation_entries

    # Main splitters

    def split_forms(self):
        """
        Splits a "forms" string into main form, oblique forms and word comment
        :return: {'main': split_wf(forms), 'comment': comment,
                  'oblique': {formN: split_wf(forms), formM: split_wf(forms), ...}}
        """
        oblique_forms = {}
        comment = ''
        forms_text = self.lexeme_entry.forms_text.strip()
        forms_split = RE_FORM.split(forms_text)
        for i in range(1, len(forms_split), 2):
            form_object = self.get_form(forms_split[i].strip(), self.lexeme_entry.language)
            oblique_forms[form_object] = self._split_wf(forms_split[i+1].strip())
        # TODO Check that the first element is not empty
        main_comment = RE_COMMENT.split(forms_split[0].strip(), 1)

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
        rel_dests = tuple(rel.strip() for rel in relations.pop().split('+'))
        rel_type = RELATION_TYPES[relations.pop().lower()]
        return {rel_type: rel_dests}

    def split_translations(self):
        """

        :return: {language: [semantic_groups, ...]}
        """
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
        sources = tuple(source.strip().split(':') for source in sources_text.split(';'))
        return ({'source': source[0].strip(), 'entry': source[1].strip()} for source in sources)


class LexemeEntry(LanguageEntity):
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
    disambig = models.CharField(max_length=64, default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Parser = LexemeEnrtyParser(self)
        self.old_version = None
        self.unsaved_wordform_spellings = []

    def get_absolute_url(self):
        if self.disambig:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug, 'disambig': self.disambig})
        else:
            return reverse('wordengine:view_lexeme_entry', kwargs={'lang_code': self.language.iso_code,
                                                                   'slug': self.slug})

    def new_or_changed(self, field):
        return (self.pk is None) or (self.pk is not None and getattr(self, field) != getattr(self.old_version, field))

    def save(self, *args, **kwargs):
        saving_reverse = kwargs.pop('reverse', False)

        # Determine if the object is new or not
        if self.pk:
            # Get an original object
            self.old_version = LexemeEntry.objects.get(pk=self.id)

        # Compare field by field
        if self.new_or_changed('forms_text'):
            # Update slug and disambig
            self.slug = slugify.slugify(self.mainform_caption, spaces=True, lower=False)
            if self.new_or_changed('slug'):
                # Check if disambiguation is needed and if it is, use plain numbering
                existant_entries = LexemeEntry.objects.filter(slug=self.slug, language=self.language)
                if existant_entries.count() == 1:
                    existant_entry = existant_entries[0]
                    existant_entry.disambig = '1'
                    existant_entry.save()
                    self.disambig = '2'
                elif existant_entries.count() > 1:
                    self.disambig = int(existant_entries.aggregate(models.Max('disambig'))['disambig__max']) + 1

            # Update corresponding wordform spelling objects
            self.unsaved_wordform_spellings = self.generate_wordform_spellings()

        if self.disambig:
            self.disambig_part = '({})'.format(self.disambig)
        else:
            self.disambig_part = ''

        if self.new_or_changed('relations_text'):
            pass

        if self.new_or_changed('translations_text') and not saving_reverse:
            # Get to lists: added translations and deleted translations
            import itertools
            # deleted_translations = list(itertools.filterfalse(lambda x: x in self.flat_translations,
            #                                                   self.old_version.flat_translations))
            # added_translations = list(itertools.filterfalse(lambda x: x in self.old_version.flat_translations,
            #                                                 self.flat_translations))
            # print(added_translations)
            # self.remove_translations(deleted_translations)
            new_translations = self.modify_translations()
            self.serialize_translations(new_translations)
            return None

        if self.new_or_changed('sources_text'):
            pass

        return super().save(*args, **kwargs)

    def modify_translations(self):
        new_translations = self.translations
        return new_translations

    def remove_translations(self, deleted_translations):
        for translation in deleted_translations:
            try:
                target = LexemeEntry.objects.get(**translation)
            except MultipleObjectsReturned as e:
                # TODO: Need custom logic if disambiguation required
                raise e
            except ObjectDoesNotExist:
                # TODO: Do something (it should not happen normally)
                pass
            else:
                pass

    def generate_translations(self):
        # for each translation
        for translation in self.flat_translations:
            try:
                target = LexemeEntry.objects.get(**translation)
            except MultipleObjectsReturned as e:
                # TODO: Need custom logic if disambiguation required
                raise e
            except ObjectDoesNotExist:
                target = LexemeEntry()
                target.language = translation['language']
                target.dictionary = self.dictionary
                target.reverse_generated = True
                target.syntactic_category = self.syntactic_category
                target.forms_text = translation['word']
                target.translations_text = '{{{0}}}\r\n1. $:{1}{2}'.format(self.language.iso_code, self.slug,
                                                                           self.disambig_part)
            else:
                reverse_found = False
                language_group = target.translations.get(self.language)
                if language_group:
                    for target_sg in language_group:
                        for target_transl in target_sg['translations']:
                            if target_transl['word'] == self.slug and \
                               target_transl['disambig'] == self.disambig:
                                reverse_found = True
                else:
                    target.translations_text += '\r\n{{{}}}'.format(self.language.iso_code)
                if not reverse_found:
                    target.translations_text += '\r\n*. $:{0}{1}'.format(self.slug, self.disambig_part)
            target.save(reverse=True)
        # if translations exists, check if the other end has a reference
        # else add a reference

    @lazy
    def flat_translations(self):
        translations = self.translations
        flat_translations = []
        for language in translations:
            for semantic_group in translations[language]:
                for translation in semantic_group['translations']:
                    flat_translation = {
                        'slug': translation['word'],
                        'language': language,
                    }
                    if translation['disambig']:
                        flat_translation['disambig'] = translation['disambig']
                    flat_translations.append(flat_translation)
        return flat_translations

    def serialize_translations(self, translations):
        translation_parts = []
        for language in sorted(translations, key=lambda lang: lang.iso_code):
            translation_parts.append('{{{}}}'.format(language.iso_code))
            for sg_num, semantic_group in enumerate(translations[language]):
                dialects = ' '.join(['<{}>'.format(dialect.term_abbr) for dialect in semantic_group['dialects']])
                if semantic_group['comment']:
                    group_comment = ' """{}"""'.format(semantic_group['comment'])
                else:
                    group_comment = ''
                translation_parts.append('{0}. {1}{2}'.format(sg_num+1, dialects, group_comment))
                translation_targets = []
                for translation in semantic_group['translations']:
                    if translation['is_reverse']:
                        tr_main = '$:{}'.format(translation['word'])
                    else:
                        tr_main = translation['word']
                    if translation['disambig']:
                        disambig = ' ({})'.format(translation['disambig'])
                    else:
                        disambig = ''
                    if translation['comment']:
                        comment = ' """{}"""'.format(translation['comment'])
                    else:
                        comment = ''
                    if translation['examples']:
                        examples = '\r\n>>' + '\r\n>> '.join(translation['examples'])
                    else:
                        examples = ''
                    translation_targets.append('{0}{1}{2}{3}'.format(tr_main, disambig, comment, examples))
                translation_parts.append('; '.join(translation_targets))
        print('\r\n'.join(translation_parts))


    def generate_wordform_spellings(self):
        WordformSpelling.objects.filter(lexeme_entry=self).delete()
        wordform_spellings = []
        wordforms = self.all_forms
        for form in wordforms:
            for wordform in wordforms[form]:
                for num, spelling in enumerate(wordform['spellings']):
                    wf_spell = WordformSpelling(lexeme_entry=self, spelling=spelling, gramm_category_set=form,
                                                writing_system=self.dictionary.get_ws(num))
                    wf_spell.dialects_list = wordform['dialects']
        return wordform_spellings

    def __str__(self):
        return ' | '.join(str(s) for s in [self.mainform_caption,  self.language, self.syntactic_category])

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
    writing_system = models.ForeignKey(WritingSystem, editable=False)

    def __str__(self):
        return 'Entry {0}. {1} : {2}, {3} ({4})'.format(self.lexeme_entry, self.spelling, self.gramm_category_set,
                                                        self.dialects, self.writing_system)