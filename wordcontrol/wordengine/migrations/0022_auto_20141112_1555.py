# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0021_auto_20141111_2350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grammcategoryset',
            old_name='gramm_category_multi',
            new_name='gramm_category_m',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='syntactic_category_multi',
            new_name='syntactic_category_m',
        ),
        migrations.RenameField(
            model_name='projectcolumnliteral',
            old_name='dialect',
            new_name='dialect_l',
        ),
        migrations.RenameField(
            model_name='projectcolumnliteral',
            old_name='language',
            new_name='language_l',
        ),
        migrations.RenameField(
            model_name='projectcolumnliteral',
            old_name='processing',
            new_name='processing_l',
        ),
        migrations.RenameField(
            model_name='projectcolumnliteral',
            old_name='source',
            new_name='source_l',
        ),
        migrations.RenameField(
            model_name='projectcolumnliteral',
            old_name='writing_system',
            new_name='writing_system_l',
        ),
        migrations.RenameField(
            model_name='projectlexemeliteral',
            old_name='params',
            new_name='params_l',
        ),
        migrations.RenameField(
            model_name='projectlexemeliteral',
            old_name='syntactic_category',
            new_name='syntactic_category_l',
        ),
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='dialect_multi',
            new_name='dialect_m',
        ),
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='usage_constraint_multi',
            new_name='usage_constraint_m',
        ),
        migrations.RenameField(
            model_name='projectsemanticgroupliteral',
            old_name='params',
            new_name='dialect_l',
        ),
        migrations.RenameField(
            model_name='projectwordformliteral',
            old_name='lexeme',
            new_name='lexeme_l',
        ),
        migrations.RenameField(
            model_name='projectwordformliteral',
            old_name='params',
            new_name='params_l',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='dialect_multi',
            new_name='dialect_m',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='source_multi',
            new_name='source_m',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='theme',
            new_name='theme_m',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='usage_constraint_multi',
            new_name='usage_constraint_m',
        ),
        migrations.RenameField(
            model_name='translation',
            old_name='source_multi',
            new_name='source_m',
        ),
        migrations.RenameField(
            model_name='wordform',
            old_name='dialect_multi',
            new_name='dialect_m',
        ),
        migrations.RenameField(
            model_name='wordform',
            old_name='source_multi',
            new_name='source_m',
        ),
        migrations.RenameField(
            model_name='wordformsample',
            old_name='source_multi',
            new_name='source_m',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='translation_based_multi',
        ),
        migrations.AddField(
            model_name='projectcolumn',
            name='processing_type_1',
            field=models.CharField(choices=[('NP', 'No processing'), ('WS', 'Writing system changed')], max_length=2, default='N'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectsemanticgroupliteral',
            name='params_l',
            field=models.CharField(max_length=256, default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='translation_based_m',
            field=models.ManyToManyField(null=True, related_name='translation_based_m_rel_+', to='wordengine.Translation', blank=True),
            preserve_default=True,
        ),
    ]
