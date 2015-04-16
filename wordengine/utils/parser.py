import re

RE_DIALECT = re.compile(r'<(.*?)>')
RE_FORM = re.compile(r'\{(.*?)\}')
RE_COMMENT = re.compile(r'"""(.*?)"""')
RE_GROUP_COMMENT = re.compile(r'^"""(.*?)"""')
RE_SEM_GR = re.compile(r'^[\d\*]\.', re.M)
RE_TRANSL = re.compile(r'^{(.*?)}', re.M)
RE_EXAMPLE = re.compile(r'>>(.*?)', re.M)
RELATION_TYPES = {
    'pl': 'Plurale tantum',
    'phr': 'Phrase'
}

def split_wf(wf_literal):
    """
    Splits a string of wordforms, separated by comma.
    Then pops a dialect mark from the wordform.
    :param wf_literal: 'Wordform1=Wordform1_alt, Wordform2=Wordform2_alt <Dialect>, ..., WordformN'
    :return: [([Wordform1, Wordform1_alt], []), ([Wordform2, Wordform2_alt], [Dialect]), ([WordformN], [])]
    """

    wordforms = []

    for wordform in wf_literal.split(','):
        dialects = []
        wf_dialect = RE_DIALECT.split(wordform.strip())
        # TODO Check that the first element is not empty
        # TODO Check that there is nothing between dialects
        while len(wf_dialect) > 1:
            wf_dialect.pop()
            dialects.append(wf_dialect.pop())
        spellings = wf_dialect.pop().split('=')
        wordforms.append((spellings, dialects))

    return wordforms


def split_forms(forms_text):
    """
    Splits a "forms" string into main form, oblique forms and word comment
    :param forms_text:
    :return:
    """
    oblique_forms = {}
    comment = ''

    forms_split = RE_FORM.split(forms_text)
    for i in range(1, len(forms_split), 2):
        oblique_forms[forms_split[i].strip()] = split_wf(forms_split[i+1].strip())
    # TODO Check that the first element is not empty
    main_comment = RE_COMMENT.split(forms_split[0].strip(), 1)

    if len(main_comment) == 3:
        # TODO Check that the last element is empty
        main_comment.pop()
        comment = main_comment.pop()
    main_form = split_wf(main_comment.pop())

    forms = {'main': main_form, 'comment': comment, 'oblique': oblique_forms}
    return forms


def split_transl_entry(transl_entry):
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
    word = comm_split[0].strip()
    if word[:2] == '$:':
        is_reverse = True
        word = word[2:].strip()
    else:
        is_reverse = False
    return {'word': word, 'comment': comment, 'examples': examples, 'is_reverse': is_reverse}


def split_semantic_groups(language_group):
    semanitc_groups = RE_SEM_GR.split(language_group)
    translation_entries = []
    # TODO Check that the first element is empty
    for semanitc_group in semanitc_groups[1:]:
        sem_gr_spl = RE_DIALECT.split(semanitc_group.strip())
        comm_transl = RE_GROUP_COMMENT.split(sem_gr_spl.pop().strip(), 1)
        translations = (split_transl_entry(translation) for translation in comm_transl.pop().strip().split(';'))
        if len(comm_transl) > 1:
            comment = comm_transl.pop()
        else:
            comment = ''
        # TODO Check that the first element is empty
        dialects = []
        while len(sem_gr_spl) > 1:
            # TODO Check if there are only empty elements between dialect marks
            # TODO Add support to place comment in front of dialects list
            dialects.append(sem_gr_spl.pop())
            sem_gr_spl.pop()

        # TODO Add semantic group order
        translation_entries.append({'comment': comment, 'dialects': dialects,
                                    'translations': translations})
    return translation_entries

def split_translations(translations_text):
    # TODO Check that the first element is empty
    transl_spl = RE_TRANSL.split(translations_text)
    translations = {}
    for i in range(1, len(transl_spl), 2):
        translations[transl_spl[i]] = split_semantic_groups(transl_spl[i+1])
    print(translations)
    return translations


def split_relations(relations_text):
    relations = relations_text.split(':', 1)
    rel_dests = (rel.strip() for rel in relations.pop().split('+'))
    rel_type = RELATION_TYPES[relations.pop().lower()]
    return {rel_type: rel_dests}


def split_sources(sources_text):
    sources = (source.strip().split(':') for source in sources_text.split(';'))
    return ({'source': source[0].strip(), 'entry': source[1].strip()} for source in sources)
