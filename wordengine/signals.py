from django.db.models.signals import post_save
from django.dispatch import receiver

from wordengine import models

# TODO Using signals in this case breaks atomicity
@receiver(post_save, sender=models.LexemeEntry)
def lexeme_entry_post_save(sender, **kwargs):
    lexeme_entry = kwargs['instance']
    if lexeme_entry.unsaved_wordform_spellings:
        for spelling in lexeme_entry.unsaved_wordform_spellings:
            spelling.lexeme_entry = lexeme_entry
            spelling.save()
            spelling.dialects.add(*spelling.dialects_list)