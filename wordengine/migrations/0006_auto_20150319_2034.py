# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0005_lexemeentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='sources',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='lexeme_relation_m',
            field=models.ManyToManyField(through='wordengine.Relation', related_name='relation_set', blank=True, to='wordengine.Lexeme'),
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='translation_m',
            field=models.ManyToManyField(through='wordengine.Translation', related_name='translation_set', blank=True, to='wordengine.Lexeme'),
        ),
    ]
