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

# Literal-to-real object correspondence
LITERAL_TO_REAL = {'ProjectLexemeLiteral': 'Lexeme',
                   'ProjectWordformLiteral': 'Wordform',
                   'ProjectSemanticGroupLiteral': 'SemanticGroup',
                   'ProjectTranslationLiteral': '[TRANSLATION_PLACEHOLDER]'}

LEX_PARAMS = (('param', 'Parameter'),
              ('inflection', 'Inflection'))

WF_PARAMS = (('gramm_category_set', 'Grammatical category'),
             ('dialect', 'Dialect'),
             ('informant', 'Informant'))

SEM_GR_PARAMS = (('dialect', 'Dialect'),
                 ('theme', 'Theme'))
