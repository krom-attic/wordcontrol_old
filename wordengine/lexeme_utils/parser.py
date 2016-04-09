from collections import namedtuple
import re

import slugify

from wordengine.global_const import TRANSLATION_MARKS, RELATION_TYPES
from wordengine.model.dialect import Dialect
from wordengine.model.gramm_category_set import GrammCategorySet
from wordengine.model.language import Language

RE_DIALECT = re.compile(r'<(.*?)>')
RE_EXAMPLE = re.compile(r'>>(.*?)', re.M)
RE_COMMENT = re.compile(r'"""(.*?)"""')
RE_DISAMBIG = re.compile(r'\((.*?)\)')
RE_SEM_GR = re.compile(r'^[\d\*]\.', re.M)
RE_GROUP_COMMENT = re.compile(r'^"""(.*?)"""')
RE_FORM = re.compile(r'\{(.*?)\}')
RE_TRANSL = re.compile(r'^{(.*?)}', re.M)

Relation = namedtuple('Relation', ['caption_form', 'slug'])


class LexemeEnrtyParser:

    lexeme_entry = None

    def __init__(self, lexeme_entry):
        self.lexeme_entry = lexeme_entry

    # Helper splitters

    def _split_wf(self, wf_literal):
        """
        Splits a string of wordforms, separated by comma.
        Then pops a dialect mark from the wordform.
        :param wf_literal: 'Wordform1=Wordform1_alt, Wordform2=Wordform2_alt <Dialect>, ..., WordformN'
        :return: [{'spellings': [Wordform1, Wordform1_alt], 'dialects': [], 'wf_type': '..'}, {'spellings':
                  [Wordform2, Wordform2_alt], 'dialects': [Dialect], 'wf_type': '..'}, {'spellings': [WordformN],
                   'dialects': [], 'wf_type': '..'}]
        """

        wordforms = []

        for wordform in wf_literal.split(';'):
            dialects = []
            wf_dialect = RE_DIALECT.split(wordform.strip())
            # TODO Check that the first element is not empty
            # TODO Check that there is nothing between dialects
            while len(wf_dialect) > 1:
                wf_dialect.pop()
                dialects.append(Dialect.get_dialect_by_abbr(wf_dialect.pop().strip(), self.lexeme_entry.language))
            spelling_group = wf_dialect.pop()
            # TODO Check that the first and the last element are paired for // and []
            if spelling_group[0] == '/':
                wf_type = 'PL'
            elif spelling_group[0] == '[':
                wf_type = 'PS'
            else:
                wf_type = 'O'
            spellings = spelling_group.split('=')
            wordforms.append({'spellings': spellings, 'dialects': dialects, 'wf_type': wf_type})

        return wordforms

    @staticmethod
    def _split_transl_entry(transl_entry):
        """

        :param transl_entry: $:translation (1) "" "Comment" "" \r\n >> Example
        :return: {'caption_form': caption_form, 'disambig': disambig, 'comment': comment, 'examples': examples,
                  'state': state, 'slug': slug}
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
            disambig = int(word_split[1].strip())
        else:
            disambig = None
        state = TRANSLATION_MARKS.get(word_split[0][:2], '')
        if state:
            caption_form = word_split[0][2:].strip()
        else:
            caption_form = word_split[0].strip()
        slug = slugify.slugify(caption_form, spaces=True, lower=False)
        return {'caption_form': caption_form, 'disambig': disambig, 'comment': comment, 'examples': examples,
                'state': state, 'slug': slug}

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
            translations = [self._split_transl_entry(translation)
                            for translation in comm_transl.pop().strip().split(';')]
            if len(comm_transl) > 1:
                comment = comm_transl.pop()
            else:
                comment = ''
            # TODO Check that the first element is empty
            dialects = []
            while len(sem_gr_spl) > 1:
                # TODO Check if there are only empty elements between dialect marks
                # TODO Add support to place comment in front of dialects list
                dialects.append(Dialect.get_dialect_by_abbr(sem_gr_spl.pop().strip(), self.lexeme_entry.language))
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
            form_object = GrammCategorySet.get_form_by_abbr(forms_split[i].strip(), self.lexeme_entry.language)
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
        """

        :return: {rel_type: [(caption_form=rel_dest, slug=rel_dest_slug), ...]
        """

        relations_text = self.lexeme_entry.relations_text.strip()
        if not relations_text:
            return {}
        relations = relations_text.split(':', 1)
        rel_dests = [Relation(rel.strip(), slugify.slugify(rel.strip(), spaces=True, lower=False))
                     for rel in relations.pop().split('+')]
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
            language = Language.get_language_by_code(transl_spl[i])
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
