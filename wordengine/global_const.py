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

# Processing types
PROC_TYPE = (('NP', 'No processing'),
             ('WS', 'Writing system changed'), )

#  TODO Obsolete???
WORD_SOURCE_CHOICES = (('NN', 'Not needed'),
                       ('AT', 'As for translation'))

# Projected objects to real objects correspondence
PRJ_TO_REAL = {'ProjectLexeme': 'Lexeme',
               'ProjectWordform': 'Wordform',
               'ProjectSemanticGroup': 'Semantic Group'}

# Variants of terms available for different projected fields
TERM_TYPES = {('Lexeme', 'syntactic_category'): 'SyntacticCategory',
              ('Lexeme', 'params'): (('lexeme parameter', 'Lexeme parameter'),
                                     ('inflection', 'Inflection')),
              ('Wordform', 'params'): (('dialect', 'Dialect'),
                                       ('gramm category set', 'Grammatical Category'),
                                       ('informant', 'Informant')),
              ('Semantic Group', 'params'): (('dialect', 'Dialect'),
                                             ('theme', 'Theme'))}

REL_DIRECTION = (('F', 'Forward'),
                 ('B', 'Backward'),
                 ('D', 'Duplex'))