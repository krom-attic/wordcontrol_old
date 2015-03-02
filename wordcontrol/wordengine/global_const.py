import re

APP_NAME = ('wordengine')


TRANSCRIPT_BRACKETS = {
    'PS': ('[{}]'),
    'PL': ('/{}/')
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
RE_PARAM = re.compile(r'(\[.*?\])')
RE_COMMENT = re.compile(r'(\".*?\")')
RE_REST_LIST = re.compile(r'\[.*\]')
RE_REST_TUPLE = re.compile(r'\(.*\)')

ERRORS = {
    'CSV-1': 'Unexpected parameters at the beginning: ',
    'CSV-2': 'No essential data',
    'CSV-3': 'Unexpected data between "]" and "[": ',
    'CSV-4': 'Unexpected data between brackets and quotes (parameters and comment): ',
    'CSV-5': 'Unexpected data after quotes (must be used only for comments)',
    'CSV-6': 'Unexpected comment: ',
    'CSV-7': 'Unused special symbol: ',
    'CSV-8': 'Excessive extended comments marks: ',
    'CSV-9': 'No lexeme in the row',
    'CSV-10': 'Something odd is in extended comment cell'
}