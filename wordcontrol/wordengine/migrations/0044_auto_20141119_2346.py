# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0043_auto_20141119_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='translation',
            old_name='source',
            new_name='source_m',
        ),
        migrations.RenameField(
            model_name='wordform',
            old_name='source',
            new_name='source_m',
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='source_m',
            field=models.ManyToManyField(through='wordengine.DictSemanticGroup', to='wordengine.Source'),
            preserve_default=True,
        ),
    ]
