from django.contrib import admin

from wordengine import models

# Inline admin views


class SyntCatsInLanguageInline(admin.TabularInline):
    model = models.SyntCatsInLanguage
    extra = 1


class LanguageAdmin(admin.ModelAdmin):
    inlines = (SyntCatsInLanguageInline, )


class WSInDictInline(admin.TabularInline):
    model = models.WSInDict
    extra = 1
    ordering = ("language", "order", )


class DictionaryAdmin(admin.ModelAdmin):
    inlines = (WSInDictInline, )


admin.site.register(models.SyntacticCategory)
admin.site.register(models.UsageConstraint)
admin.site.register(models.GrammCategory)
admin.site.register(models.GrammCategorySet)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Dialect)
admin.site.register(models.WritingSystem)
admin.site.register(models.Lexeme)
admin.site.register(models.Wordform)
admin.site.register(models.Translation)
admin.site.register(models.TranslatedTerm)
admin.site.register(models.Source)
admin.site.register(models.GrammCategoryType)
admin.site.register(models.LexemeParameter)
admin.site.register(models.SyntCatsInLanguage)
admin.site.register(models.Theme)
admin.site.register(models.Dictionary, DictionaryAdmin)
admin.site.register(models.WSInDict)
