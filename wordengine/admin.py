__author__ = 'Blane'

from django.contrib import admin
import wordengine.models

admin.site.register(wordengine.models.SyntacticCategory)
admin.site.register(wordengine.models.UsageConstraint)
admin.site.register(wordengine.models.Animacy)
admin.site.register(wordengine.models.Aspect)
admin.site.register(wordengine.models.Case)
admin.site.register(wordengine.models.Comparison)
admin.site.register(wordengine.models.Gender)
admin.site.register(wordengine.models.Mood)
admin.site.register(wordengine.models.Number)
admin.site.register(wordengine.models.Person)
admin.site.register(wordengine.models.Polarity)
admin.site.register(wordengine.models.Tense)
admin.site.register(wordengine.models.Voice)
admin.site.register(wordengine.models.GrammCategorySet)
admin.site.register(wordengine.models.Language)
admin.site.register(wordengine.models.Dialect)
admin.site.register(wordengine.models.WritingSystem)
admin.site.register(wordengine.models.WritingSystemType)
admin.site.register(wordengine.models.Lexeme)
admin.site.register(wordengine.models.WordForm)
admin.site.register(wordengine.models.Translation)
admin.site.register(wordengine.models.TranslatedTerm)


