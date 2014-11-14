# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0031_auto_20141114_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='theme',
            new_name='theme_r',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='dialect',
            new_name='dialect_r',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='gramm_category_set',
            new_name='gramm_category_set_r',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='informant',
            new_name='informant_r',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='inflection',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='syntactic_category',
        ),
    ]
