from django.db import models
from django.contrib import auth

# Global abstract classes


class Change(models.Model):
    """Abstract base class representing submitted change."""

    user_changer = models.ForeignKey(auth.models.User, editable=False, related_name="%(app_label)s_%(class)s_changer")
    timestamp_change = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField()

    class Meta:
        abstract = True


class MiscChange(Change):
    table_name = models.CharField()
    field_name = models.CharField()
    old_value = models.CharField()
    new_value = models.CharField()


# Dictionary term models


class Term(models.Model):
    """Abstract base class for all terms in dictionary."""

    term_full = models.CharField()
    term_abbr = models.CharField()

    class Meta:
        abstract = True


class SyntacticCategory(Term):
    pass


class UsageConstraints(Term):
    pass


class Animacy(Term):
    pass


class Aspect(Term):
    pass


class Case(Term):
    pass


class Comparison(Term):
    pass


class Gender(Term):
    pass


class Mood(Term):
    pass


class Number(Term):
    pass


class Person(Term):
    pass


class Polarity(Term):
    pass


class Tense(Term):
    pass


class Voice(Term):
    pass


class GrammarCategorySet(models.Model):
    animacy = models.ForeignKey(null=True)
    aspect = models.ForeignKey(null=True)
    case = models.ForeignKey(null=True)
    comparison = models.ForeignKey(null=True)
    gender = models.ForeignKey(null=True)
    mood = models.ForeignKey(null=True)
    number = models.ForeignKey(null=True)
    person = models.ForeignKey(null=True)
    polarity = models.ForeignKey(null=True)
    tense = models.ForeignKey(null=True)
    voice = models.ForeignKey(null=True)

