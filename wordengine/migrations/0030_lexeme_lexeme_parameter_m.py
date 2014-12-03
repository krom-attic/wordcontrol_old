# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0029_auto_20141114_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexeme',
            name='lexeme_parameter_m',
            field=models.ManyToManyField(null=True, blank=True, to='wordengine.LexemeParameter'),
            preserve_default=True,
        ),
    ]
