# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectColumn',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('default_dialect', models.ForeignKey(null=True, blank=True, to='wordengine.Dialect')),
                ('language', models.ForeignKey(to='wordengine.Language')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('source', models.ForeignKey(null=True, blank=True, to='wordengine.Source')),
                ('writing_system', models.ForeignKey(to='wordengine.WritingSystem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectColumnLiteral',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('language', models.CharField(blank=True, max_length=256)),
                ('default_dialect', models.CharField(blank=True, max_length=256)),
                ('writing_system', models.CharField(blank=True, max_length=256)),
                ('source', models.CharField(blank=True, max_length=256)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLexeme',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('inflection', models.ForeignKey(null=True, blank=True, to='wordengine.Inflection')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('syntactic_category', models.ForeignKey(to='wordengine.SyntacticCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLexemeLiteral',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('syntactic_category', models.CharField(max_length=256)),
                ('inflection', models.CharField(blank=True, max_length=256)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('comment_1', models.TextField(blank=True)),
                ('comment_2', models.TextField(blank=True)),
                ('dialect_1', models.ForeignKey(null=True, blank=True, related_name='translation_fst_set', to='wordengine.Dialect')),
                ('dialect_2', models.ForeignKey(null=True, blank=True, related_name='translation_snd_set', to='wordengine.Dialect')),
                ('lexeme_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectLexeme')),
                ('lexeme_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectLexeme')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('theme', models.ForeignKey(null=True, blank=True, to='wordengine.Theme')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTranslationLiteral',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('theme', models.CharField(blank=True, max_length=256)),
                ('dialect_1', models.CharField(blank=True, max_length=256)),
                ('dialect_2', models.CharField(blank=True, max_length=256)),
                ('comment_1', models.TextField(blank=True)),
                ('comment_2', models.TextField(blank=True)),
                ('lexeme_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectLexemeLiteral')),
                ('lexeme_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectLexemeLiteral')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWordform',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('wordform', models.CharField(max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('informant', models.CharField(blank=True, max_length=256)),
                ('dialect', models.ForeignKey(null=True, blank=True, to='wordengine.Dialect')),
                ('gramm_category_set', models.ForeignKey(null=True, blank=True, to='wordengine.GrammCategorySet')),
                ('lexeme', models.ForeignKey(to='wordengine.ProjectLexeme')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWordformLiteral',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('col_num', models.SmallIntegerField()),
                ('wordform', models.CharField(max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('gramm_category_set', models.CharField(blank=True, max_length=256)),
                ('dialect', models.CharField(blank=True, max_length=256)),
                ('informant', models.CharField(blank=True, max_length=256)),
                ('lexeme', models.ForeignKey(to='wordengine.ProjectLexemeLiteral')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='columndata',
            name='language',
        ),
        migrations.RemoveField(
            model_name='columndata',
            name='project',
        ),
        migrations.DeleteModel(
            name='ColumnData',
        ),
        migrations.RemoveField(
            model_name='lexemeproject',
            name='project',
        ),
        migrations.DeleteModel(
            name='LexemeProject',
        ),
        migrations.DeleteModel(
            name='RelationType',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='source',
            new_name='source_multi',
        ),
        migrations.RenameField(
            model_name='translation',
            old_name='source',
            new_name='source_multi',
        ),
        migrations.RenameField(
            model_name='wordform',
            old_name='source',
            new_name='source_multi',
        ),
        migrations.RenameField(
            model_name='wordformsample',
            old_name='source',
            new_name='source_multi',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='translation_based',
        ),
        migrations.AddField(
            model_name='dialect',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grammcategory',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grammcategorytype',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='language',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='language',
            name='iso_code',
            field=models.CharField(max_length=8, default='zzz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lexemerelation',
            name='relation_type',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='syntacticcategory',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='translation_based_multi',
            field=models.ManyToManyField(related_name='translation_based_multi_rel_+', to='wordengine.Translation', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usageconstraint',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='syntactic_category',
            field=models.ForeignKey(to='wordengine.SyntacticCategory'),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_type',
            field=models.SmallIntegerField(),
        ),
        migrations.DeleteModel(
            name='SourceType',
        ),
        migrations.AlterField(
            model_name='writingsystem',
            name='writing_system_type',
            field=models.SmallIntegerField(),
        ),
        migrations.DeleteModel(
            name='WritingSystemType',
        ),
    ]
