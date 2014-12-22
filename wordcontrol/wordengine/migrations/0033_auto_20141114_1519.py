# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0032_auto_20141114_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectlexeme',
            old_name='params_l',
            new_name='params',
        ),
        migrations.RenameField(
            model_name='projectlexeme',
            old_name='syntactic_category_l',
            new_name='syntactic_category',
        ),
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='dialect_l',
            new_name='dialect',
        ),
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='params_l',
            new_name='params',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='lexeme_l',
            new_name='lexeme',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='params_l',
            new_name='params',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='dialect_m',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='theme_r',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='usage_constraint_m',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='dialect_r',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='gramm_category_set_r',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='informant_r',
        ),
    ]
