from django.db.models.signals import post_save
from django.dispatch import receiver

from wordengine import models

# TODO Using signals in this case breaks atomacity
@receiver(post_save, sender=models.LexemeEntry)
def lexeme_entry_pre_save(sender, **kwargs):
    lexeme_entry = kwargs['instance']
    if lexeme_entry.need_spelling_update:
        lexeme_entry.generate_wordform_spellings()
    if lexeme_entry.need_translations_update:
        lexeme_entry.generate_translations()