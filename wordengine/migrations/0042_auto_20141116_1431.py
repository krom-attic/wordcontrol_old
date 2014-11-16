# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0041_auto_20141115_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectlexeme',
            name='result',
            field=models.ForeignKey(to='wordengine.Lexeme', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectsemanticgroup',
            name='result',
            field=models.ForeignKey(to='wordengine.SemanticGroup', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttranslation',
            name='result',
            field=models.ForeignKey(to='wordengine.Translation', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordform',
            name='result',
            field=models.ForeignKey(to='wordengine.Wordform', blank=True, null=True),
            preserve_default=True,
        ),
    ]
