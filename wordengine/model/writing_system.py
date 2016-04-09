from django.db import models

from wordengine.model.language import Language
from wordengine.model.term import Term
from wordengine.model.writing_related import WritingRelated


class WritingSystem(Term, WritingRelated):
    """Class represents a writing systems used to spell a word form"""

    language = models.ForeignKey(Language, null=True, blank=True)  # Null means "language independent"

