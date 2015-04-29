# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0013_auto_20150417_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='disambig',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='syntactic_category_m',
            field=models.ManyToManyField(through='wordengine.SyntCatsInLanguage', blank=True, to='wordengine.SyntacticCategory', related_name='synt_cat_set'),
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='lexeme_parameter_m',
            field=models.ManyToManyField(blank=True, to='wordengine.LexemeParameter'),
        ),
        migrations.AlterField(
            model_name='semanticgroup',
            name='dialect_m',
            field=models.ManyToManyField(blank=True, to='wordengine.Dialect'),
        ),
        migrations.AlterField(
            model_name='semanticgroup',
            name='theme_m',
            field=models.ManyToManyField(blank=True, to='wordengine.Theme'),
        ),
        migrations.AlterField(
            model_name='semanticgroup',
            name='usage_constraint_m',
            field=models.ManyToManyField(blank=True, to='wordengine.UsageConstraint'),
        ),
        migrations.AlterField(
            model_name='wordform',
            name='dialect_m',
            field=models.ManyToManyField(blank=True, to='wordengine.Dialect'),
        ),
        migrations.AlterField(
            model_name='wordformspelling',
            name='dialects',
            field=models.ManyToManyField(blank=True, to='wordengine.Dialect', editable=False),
        ),
    ]
