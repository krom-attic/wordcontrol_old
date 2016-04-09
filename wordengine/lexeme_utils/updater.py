from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from slugify import slugify

from wordengine.global_const import TRANSLATION_MARKS
from wordengine.model.lexeme_entry import LexemeEntry
from wordengine.model.wordform_spelling import WordformSpelling


def new_or_changed(entry, old_version, field):
    return (entry.pk is None) or (entry.pk is not None and getattr(entry, field) != getattr(old_version, field))


def update_slug_disambig(entry):
    existant_entries = LexemeEntry.objects.filter(slug=entry.slug, language=entry.language)
    if existant_entries.count() == 1:
        existant_entry = existant_entries[0]
        existant_entry.disambig = 1
        entry.disambig = 2
        return [existant_entry]
    elif existant_entries.count() > 1:
        entry.disambig = int(existant_entries.aggregate(models.Max('disambig'))['disambig__max']) + 1
    return []


def flat_translations(entry):
    """
    Returns flattened list of translations, excluding those marked 'deleted'
    :return:
    """
    translations = []
    for language in entry.translations:
        for semantic_group in entry.translations[language]:
            translations.extend([{
                'language': language,
                'caption_form': translation['caption_form'],
                'disambig': translation['disambig'],
            } for translation in semantic_group['translations'] if translation['state'] != 'deleted'])
    return translations


def serialize_translations(translations):
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
                tr_mark = (~TRANSLATION_MARKS).get(translation['state']) if translation['state'] else ''
                disambig = ' ({})'.format(translation['disambig']) if translation['disambig'] else ''
                comment = ' """{}"""'.format(translation['comment']) if translation['comment'] else ''
                examples = '\r\n>>' + '\r\n>> '.join(translation['examples']) if translation['examples'] else ''
                translation_targets.append('{0}{1}{2}{3}{4}'.format(tr_mark, translation['caption_form'], disambig,
                                                                    comment, examples))
            translation_parts.append('; '.join(translation_targets))
    return '\r\n'.join(translation_parts)


def update_translations(entry, old_version):
    """
    Updates translation references to entry
    Works with the OLD properties of the lexeme entry (will search for an old slug and disambig)
    :return:
    """
    affected_lexeme_entries = []
    for translation in flat_translations(entry):
        try:
            target = LexemeEntry.objects.get(**translation)
        except MultipleObjectsReturned as e:
            # TODO: Need custom logic if disambiguation required? Is it possible?
            raise e
        except ObjectDoesNotExist as e:
            # TODO: Do something (it should not happen normally)
            raise e
        else:
            new_target_translations = target.translations
            for semantic_group in new_target_translations[old_version.language]:
                for target_translation in semantic_group['translations']:
                    if (target_translation['caption_form'] == old_version.caption_form and
                       target_translation['disambig'] == old_version.disambig):
                        target_translation['caption_form'] = entry.caption_form
                        target_translation['disambig'] = entry.disambig
        target.translations_text = serialize_translations(new_target_translations)
        affected_lexeme_entries.append(target)
    return affected_lexeme_entries


def add_translations(entry, added_translations):
    """
    Adds self as a translation to a every word in added_translations list
    Works with the NEW properties of the lexeme entry (will search for a new slug and disambig)
    :param added_translations:
    :return:
    """
    affected_lexeme_entries = []
    new_wordform_spellings = []

    for translation in added_translations:
        translation_to_add = {'comment': '',
                              'dialects': [],
                              'translations': [{'caption_form': entry.caption_form,
                                                'disambig': entry.disambig,
                                                'comment': '',
                                                'examples': [],
                                                'state': 'reverse'
                                                }]}
        try:
            target = LexemeEntry.objects.get(**translation)
        except MultipleObjectsReturned as e:
            # TODO: Need custom logic if disambiguation required? Is it possible?
            raise e
        except ObjectDoesNotExist:
            target = LexemeEntry()
            target.language = translation['language']
            target.dictionary = entry.dictionary
            target.reverse_generated = True
            target.syntactic_category = entry.syntactic_category
            target.forms_text = translation['caption_form']
            target, target_spellings, _ = update_lexeme_entry(target)
            new_wordform_spellings.extend(target_spellings)
            new_target_translations = {entry.language: [translation_to_add]}
        else:
            new_target_translations = target.translations
            new_target_translations.setdefault(entry.language, []).append(translation_to_add)
        target.translations_text = serialize_translations(new_target_translations)
        affected_lexeme_entries.append(target)
    return affected_lexeme_entries, new_wordform_spellings


def remove_translations(entry, deleted_translations):
    """
    Removes self as a translation from every word in deleted_translations list
    Works with the NEW properties of the lexeme entry (will search for a new slug and disambig)
    :param deleted_translations:
    :return:
    """
    affected_lexeme_entries = []
    for translation in deleted_translations:
        try:
            target = LexemeEntry.objects.get(**translation)
        except MultipleObjectsReturned as e:
            # TODO: Do something (it should not happen normally)
            raise e
        except ObjectDoesNotExist as e:
            # TODO: Do something (it should not happen normally)
            raise e
        else:
            new_target_translations = target.translations
            for semantic_group in new_target_translations[entry.language][:]:
                for target_translation in semantic_group['translations'][:]:
                    if (target_translation['caption_form'] == entry.caption_form and
                       target_translation['disambig'] == entry.disambig):
                        if target_translation['state'] == 'reverse':
                            semantic_group['translations'].remove(target_translation)
                            if not semantic_group['translations']:
                                new_target_translations[entry.language].remove(semantic_group)
                        else:
                            target_translation['state'] = 'deleted'
            if not new_target_translations[entry.language]:
                del new_target_translations[entry.language]
        target.translations_text = serialize_translations(new_target_translations)
        affected_lexeme_entries.append(target)
    return affected_lexeme_entries


def generate_wordform_spellings(entry):
    WordformSpelling.objects.filter(lexeme_entry=entry).delete()
    # TODO May be change to the following line?
    # self.wordformspelling_set.delete()
    wordform_spellings = []
    wordforms = entry.all_forms
    for form in wordforms:
        for wordform in wordforms[form]:
            for num, spelling in enumerate(wordform['spellings']):
                wf_spell = WordformSpelling(lexeme_entry=entry, spelling=spelling, gramm_category_set=form,
                                            writing_system=entry.dictionary.get_ws(num, entry.language))
                wf_spell.dialects_list = wordform['dialects']
                wordform_spellings.append(wf_spell)
    return wordform_spellings


def update_lexeme_entry(entry: LexemeEntry):
    # TODO Introduce optimistic concurrency control
    unsaved_wordform_spellings = []
    unsaved_related_lexeme_entries = []

    # Determine if the object is new or not
    if entry.pk:
        # Get an original object
        old_version = LexemeEntry.objects.get(pk=entry.id)
    else:
        old_version = None

    # Compare field by field

    if new_or_changed(entry, old_version, 'forms_text'):
        # Update caption_form, slug and disambig
        entry.caption_form = entry.mainform_caption
        entry.slug = slugify(entry.caption_form, spaces=True, lower=False)
        if new_or_changed(entry, old_version, 'slug'):
            # Check if disambiguation is needed and if it is, use plain numbering
            unsaved_related_lexeme_entries.extend(update_slug_disambig(entry))

        # If forms are changed, translation references have to be updated
        # TODO It's enough to caption form and disambig be changed
        # TODO It may be optimized: update only translations which are still present after deletion
        if entry.pk:
            unsaved_related_lexeme_entries.extend(update_translations(entry, old_version))

        # Update corresponding wordform spelling objects
        unsaved_wordform_spellings.extend(generate_wordform_spellings(entry))

    if new_or_changed(entry, old_version, 'relations_text'):
        # TODO Important! Should not mess up with entries, updated via translation & disambiguation updates
        pass

    if new_or_changed(entry, old_version, 'translations_text'):
        # Get lists of added translations and deleted translations
        if entry.pk:
            deleted_translations = [x for x in flat_translations(old_version) if x not in flat_translations(entry)]
            added_translations = [x for x in flat_translations(entry) if x not in flat_translations(old_version)]
        else:
            deleted_translations = []
            added_translations = flat_translations(entry)

        unsaved_related_lexeme_entries.extend(remove_translations(entry, deleted_translations))
        # add_translations may generate new lexemes with their own wordforms
        affected_lexemes, generated_wordforms = add_translations(entry, added_translations)
        unsaved_related_lexeme_entries.extend(affected_lexemes)
        unsaved_wordform_spellings.extend(generated_wordforms)

    if new_or_changed(entry, old_version, 'sources_text'):
        pass

    return entry, unsaved_wordform_spellings, unsaved_related_lexeme_entries
