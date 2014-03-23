__author__ = 'Blane'

from django.contrib import admin
import wordengine.models

admin.site.register(wordengine.models.SyntacticCategory)
admin.site.register(wordengine.models.UsageConstraint)
admin.site.register(wordengine.models.GrammCategory)
admin.site.register(wordengine.models.GrammCategorySet)
admin.site.register(wordengine.models.Language)
admin.site.register(wordengine.models.Dialect)
admin.site.register(wordengine.models.WritingSystem)
admin.site.register(wordengine.models.WritingSystemType)
admin.site.register(wordengine.models.Lexeme)
admin.site.register(wordengine.models.Wordform)
admin.site.register(wordengine.models.Translation)
admin.site.register(wordengine.models.TranslatedTerm)
admin.site.register(wordengine.models.Source)

