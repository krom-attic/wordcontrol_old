# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0022_auto_20141112_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcolumn',
            name='dialect',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='language',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='literal',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='source',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='writing_system',
        ),
        migrations.DeleteModel(
            name='ProjectColumn',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='inflection',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='syntactic_category',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectRelation',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='dialect_m',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='usage_constraint_m',
        ),
        migrations.DeleteModel(
            name='ProjectSemanticGroup',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='dialect',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='gramm_category_set',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='lexeme',
        ),
        migrations.DeleteModel(
            name='ProjectLexeme',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectWordform',
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='dialect',
            field=models.ForeignKey(blank=True, to='wordengine.Dialect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='language',
            field=models.ForeignKey(blank=True, to='wordengine.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='processing_type',
            field=models.CharField(choices=[('NP', 'No processing'), ('WS', 'Writing system changed')], blank=True, null=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='source',
            field=models.ForeignKey(blank=True, to='wordengine.Source', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='writing_system',
            field=models.ForeignKey(blank=True, to='wordengine.WritingSystem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectlexemeliteral',
            name='inflection',
            field=models.ForeignKey(blank=True, to='wordengine.Inflection', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectlexemeliteral',
            name='syntactic_category',
            field=models.ForeignKey(blank=True, to='wordengine.SyntacticCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectsemanticgroupliteral',
            name='dialect_m',
            field=models.ManyToManyField(blank=True, to='wordengine.Dialect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectsemanticgroupliteral',
            name='theme',
            field=models.ForeignKey(blank=True, to='wordengine.Theme', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectsemanticgroupliteral',
            name='usage_constraint_m',
            field=models.ManyToManyField(blank=True, to='wordengine.UsageConstraint', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordformliteral',
            name='dialect',
            field=models.ForeignKey(blank=True, to='wordengine.Dialect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordformliteral',
            name='gramm_category_set',
            field=models.ForeignKey(blank=True, to='wordengine.GrammCategorySet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordformliteral',
            name='informant',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
    ]
