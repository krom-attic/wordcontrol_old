import re


RE_DIALECT = re.compile(r'<(.*?)>')
RE_FORM = re.compile(r'\{(.*?)\}')
RE_COMMENT = re.compile(r'"""(.*?)"""')
RE_SEM_GR = re.compile(r'^[\d\*]\.', re.M)
RE_TRANSL = re.compile(r'^{(.*?)}', re.M)
RE_EXAMPLE = re.compile(r'>>(.*?)', re.M)


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


def split_translations(translations_text):
    semanitc_groups = RE_SEM_GR.split(translations_text)
    translations = []
    # TODO Check that the first element is empty
    for sem_gr_spl in semanitc_groups[1:]:
        trans_spl = RE_TRANSL.split(sem_gr_spl)
        comment_dialect = RE_DIALECT.split(trans_spl[0].strip())
        dialects = []
        comment = comment_dialect[0].strip('"""')
        while len(comment_dialect) > 1:
            # TODO Check if there are too many non-empty elements between dialect marks
            comment_temp = comment_dialect.pop().strip('"""')
            if comment_temp:
                comment = comment_temp
            dialects.append(comment_dialect.pop())
        translation_entries = []
        for i in range(1, len(trans_spl), 2):
            transl_entr_spl = tuple(trans.strip() for trans in trans_spl[i+1].split(';'))

            translation_entries.append({'language': trans_spl[i], 'entries': transl_entr_spl})
        translations.append({'comment': comment, 'dialects': dialects, 'translations': translation_entries})
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


class Wordform():
    def __init__(self):
        pass

