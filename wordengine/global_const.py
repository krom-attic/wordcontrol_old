# Writing system types
WS_TYPE = ((0, 'Phonetic strict'),
           (1, 'Phonetic loose'),
           (2, 'Orthographic'))

# Source types
SRC_TYPE = ((0, 'Own knowledge'),
            (1, 'Dictionary/Textbook'),
            (2, 'Scientific publication'),
            (3, 'Field archive'),
            (4, 'Other trustworthy source'))  # e.g. lesson notes

# Types of lexemes' relations
REL_TYPE = ((0, 'Translation'), )

# Projected entity states
PRJ_STATE = ((0, 'New'),
             (1, 'Processed'))

# Processing types
PROC_TYPE = ((0, 'No processing'),
             (1, 'Writing system changed'), )

#
WORD_SOURCE_CHOICES = ((0, 'Not needed'),
                       (1, 'As for translation'),)
