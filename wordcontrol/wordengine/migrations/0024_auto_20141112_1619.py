# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0023_auto_20141112_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectColumn',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('language_l', models.CharField(max_length=256)),
                ('dialect_l', models.CharField(blank=True, max_length=256, null=True)),
                ('source_l', models.CharField(blank=True, max_length=256, null=True)),
                ('writing_system_l', models.CharField(blank=True, max_length=256, null=True)),
                ('processing_l', models.CharField(blank=True, max_length=256, null=True)),
                ('num', models.SmallIntegerField()),
                ('processing_type', models.CharField(blank=True, choices=[('NP', 'No processing'), ('WS', 'Writing system changed')], max_length=2, null=True)),
                ('processing_comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect', models.ForeignKey(blank=True, to='wordengine.Dialect', null=True)),
                ('language', models.ForeignKey(blank=True, to='wordengine.Language', null=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('source', models.ForeignKey(blank=True, to='wordengine.Source', null=True)),
                ('writing_system', models.ForeignKey(blank=True, to='wordengine.WritingSystem', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLexeme',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('syntactic_category_l', models.CharField(max_length=256)),
                ('params_l', models.CharField(blank=True, max_length=512)),
                ('col', models.ForeignKey(blank=True, to='wordengine.ProjectColumn', null=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('inflection', models.ForeignKey(blank=True, to='wordengine.Inflection', null=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('syntactic_category', models.ForeignKey(blank=True, to='wordengine.SyntacticCategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectRelation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('direction', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSemanticGroup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('params_l', models.CharField(blank=True, max_length=256)),
                ('dialect_l', models.CharField(blank=True, max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect_m', models.ManyToManyField(blank=True, to='wordengine.Dialect', null=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('theme', models.ForeignKey(blank=True, to='wordengine.Theme', null=True)),
                ('usage_constraint_m', models.ManyToManyField(blank=True, to='wordengine.UsageConstraint', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWordform',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('spelling', models.CharField(max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('params_l', models.CharField(blank=True, max_length=512)),
                ('informant', models.CharField(blank=True, max_length=256)),
                ('col', models.ForeignKey(blank=True, to='wordengine.ProjectColumn', null=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect', models.ForeignKey(blank=True, to='wordengine.Dialect', null=True)),
                ('gramm_category_set', models.ForeignKey(blank=True, to='wordengine.GrammCategorySet', null=True)),
                ('lexeme_l', models.ForeignKey(to='wordengine.ProjectLexeme')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='dialect',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='language',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='source',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='writing_system',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='col',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='inflection',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='syntactic_category',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='dialect_m',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='usage_constraint_m',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='bind_wf_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='bind_wf_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='semantic_group_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='semantic_group_2',
        ),
        migrations.DeleteModel(
            name='ProjectSemanticGroupLiteral',
        ),
        migrations.DeleteModel(
            name='ProjectTranslationLiteral',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='col',
        ),
        migrations.DeleteModel(
            name='ProjectColumnLiteral',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='dialect',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='gramm_category_set',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='lexeme_l',
        ),
        migrations.DeleteModel(
            name='ProjectLexemeLiteral',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectWordformLiteral',
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='bind_wf_1',
            field=models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectWordform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='bind_wf_2',
            field=models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectWordform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='lexeme_1',
            field=models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectLexeme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='lexeme_2',
            field=models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectLexeme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='semantic_group_1',
            field=models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectSemanticGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectrelation',
            name='semantic_group_2',
            field=models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectSemanticGroup'),
            preserve_default=True,
        ),
    ]
