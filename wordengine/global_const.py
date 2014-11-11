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

# Types of lexemes' relations
REL_TYPE = (('TR', 'Translation'), )

# Projected entity states
PRJ_STATE = (('N', 'New'),
             ('P', 'Processed'))

# Processing types
PROC_TYPE = (('NP', 'No processing'),
             ('WS', 'Writing system changed'), )

#  TODO Obsolete???
WORD_SOURCE_CHOICES = (('NN', 'Not needed'),
                       ('AT', 'As for translation'))

#
PRJ_TO_REAL = {'ProjectLexemeLiteral': 'Lexeme',
               'ProjectWordformLiteral': 'Wordform',
               'ProjectSemanticGroupLiteral': 'Semantic Group'}

# Variants of terms available for different projected fields
TERM_TYPES = {('Lexeme', 'syntactic_category'): 'SyntacticCategory',
              ('Lexeme', 'params'): (('', '<not selected>'),
                                     ('Parameter', 'Lexeme parameter'),
                                     ('Inflection', 'Inflection')),
              ('Wordform', 'params'): (('', '<not selected>'),
                                       ('Dialect', 'Dialect'),
                                       ('GrammCategorySet', 'Grammatical Category'),
                                       ('Informant', 'Informant')),
              ('Semantic Group', 'params'): (('', '<not selected>'),
                                             ('Dialect', 'Dialect'),
                                             ('Theme', 'Theme'))}