import re

APP_NAME = ('wordengine')


TRANSCRIPT_BRACKETS = {
    1: ('[{}]'),
    2: ('/{}/')
}


# Writing system types
WS_TYPE = (('PS', 'Phonetic strict'),
           ('PL', 'Phonetic loose'),
           ('O', 'Orthographic'))

# Source types
SRC_TYPE = (('OK', 'Own knowledge'),
            ('DT', 'Dictionary/Textbook'),
            ('SP', 'Scientific publication'),
            ('FA', 'Field archive'),
            ('OT', 'Other trustworthy source'))  # e.g. lesson notes

# Projected entity states
PRJ_STATE = (('N', 'New'),
             ('P', 'Processed'))


#  TODO Obsolete???
WORD_SOURCE_CHOICES = (('NN', 'Not needed'),
                       ('AT', 'As for translation'))

# Projected objects to real objects correspondence
PRJ_TO_REAL = {'ProjectLexeme': 'Lexeme',
               'ProjectWordform': 'Wordform',
               'ProjectSemanticGroup': 'Semantic Group'}

# Variants of terms available for different projected fields
TERM_TYPES = {('ProjectLexeme', 'syntactic_category'): 'SyntacticCategory',
              ('ProjectLexeme', 'params'): (('lexemeparameter', 'Lexeme parameter'),
                                            ('inflection', 'Inflection')),
              ('ProjectWordform', 'params'): (('dialect', 'Dialect'),
                                              ('grammcategoryset', 'Grammatical Category'),
                                              ('informant', 'Informant')),
              ('ProjectSemantic Group', 'params'): (('dialect', 'Dialect'),
                                                    ('theme', 'Theme'))}

REL_DIRECTION = (('F', 'Forward'),
                 ('B', 'Backward'),
                 ('D', 'Duplex'))

SPECIAL_CHARS = ('[', ']', '"', '|', '@')

# Common regexps

RE_EXT_COMM = re.compile(r'(\*\d+:)')
RE_REST_LIST = re.compile(r'\[.*\]')