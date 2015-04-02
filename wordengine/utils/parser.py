import re


RE_DIALECT = re.compile(r'<(.*?)>')
RE_FORM = re.compile(r'\{(.*?)\}')
RE_COMMENT = re.compile(r'"""(.*?)"""')
RE_SEM_GR = re.compile(r'^[\d\*]\.', re.M)
RE_TRANSL = re.compile(r'^{(.*?)}', re.M)


def split_wf(wf_literal):
    wordforms = []

    for wordform in wf_literal.split(';'):
        dialects = []
        wf_dialect = RE_DIALECT.split(wordform.strip())
        if len(wf_dialect) > 1:
            # TODO Check that [0] is empty
            while len(wf_dialect) > 2:
                dialects.append(wf_dialect.pop(-2))
        spellings = wf_dialect.pop().split('=')
        wordforms.append([dialects, spellings])
    return wordforms


def split_forms(forms_text):
    oblique_forms = []
    comment = ''

    forms_split = RE_FORM.split(forms_text)
    for i in range(1, len(forms_split), 2):
        oblique_forms.append([forms_split[i].strip(), split_wf(forms_split[i+1].strip())])
    main_comment = RE_COMMENT.split(forms_split[0].strip())
    # TODO Check that [-1] is empty
    main_comment.pop()

    if len(main_comment) == 2:
        comment = main_comment.pop()
    main_form = split_wf(main_comment.pop())

    forms = {'main': main_form, 'comment': comment, 'oblique': oblique_forms}
    return forms


def split_translations(translations_text):
    semanitc_groups = RE_SEM_GR.split(translations_text)
    translations = []
    for sem_gr_spl in semanitc_groups[1:]:
        trans_spl = RE_TRANSL.split(sem_gr_spl)
        comm_dial = trans_spl[0].strip()
        translation_entries = []
        for i in range(1, len(trans_spl), 2):
            transl_entr_spl = tuple(trans.strip() for trans in trans_spl[i+1].split(';'))
            translation_entries.append({'language': trans_spl[i], 'entries': transl_entr_spl})
        translations.append({'comment_dialect': comm_dial, 'translations': translation_entries})
    return translations


def split_relations(relations_text):
    RELATION_TYPES = {
        'pl': 'Plurale tantum',
        'phr': 'Phrase'
    }
    relations = relations_text.split(':', 1)
    rel_dests = (rel.strip() for rel in relations.pop().split('+'))
    rel_type = RELATION_TYPES[relations.pop().lower()]
    return {rel_type: rel_dests}
