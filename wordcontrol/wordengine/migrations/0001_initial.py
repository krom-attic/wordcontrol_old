# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('col_num', models.SmallIntegerField()),
                ('language_lit', models.CharField(max_length=256)),
                ('default_dialect', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dialect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DictChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp_change', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('object_type', models.TextField(max_length=256, editable=False)),
                ('object_id', models.IntegerField(editable=False)),
                ('timestamp_review', models.DateTimeField(null=True, editable=False, blank=True)),
                ('user_changer', models.ForeignKey(related_name='wordengine_dictchange_changer', to=settings.AUTH_USER_MODEL, editable=False)),
                ('user_reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, editable=False, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp_change', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('object_type', models.TextField(max_length=256, editable=False)),
                ('object_id', models.IntegerField(editable=False)),
                ('field_name', models.CharField(max_length=256)),
                ('old_value', models.CharField(max_length=512, blank=True)),
                ('new_value', models.CharField(max_length=512, blank=True)),
                ('user_changer', models.ForeignKey(related_name='wordengine_fieldchange_changer', to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('position', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammCategorySet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.SmallIntegerField(null=True, blank=True)),
                ('gramm_category_multi', models.ManyToManyField(to='wordengine.GrammCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammCategoryType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inflection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lexeme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inflection', models.ForeignKey(to='wordengine.Inflection', null=True, blank=True)),
                ('language', models.ForeignKey(to='wordengine.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LexemeProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('language', models.CharField(max_length=256)),
                ('syntactic_category', models.CharField(max_length=256)),
                ('inflection', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LexemeRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lexeme_1', models.ForeignKey(related_name='relation_fst_set', to='wordengine.Lexeme')),
                ('lexeme_2', models.ForeignKey(related_name='relation_snd_set', to='wordengine.Lexeme')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SemanticGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('dialect_multi', models.ManyToManyField(to='wordengine.Dialect', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('language', models.ForeignKey(to='wordengine.Language', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SyntacticCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslatedTerm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('table', models.CharField(max_length=256)),
                ('term_id', models.IntegerField()),
                ('term_full_translation', models.CharField(max_length=256)),
                ('term_abbr_translation', models.CharField(max_length=64, blank=True)),
                ('language', models.ForeignKey(to='wordengine.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('direction', models.PositiveSmallIntegerField()),
                ('is_visible', models.BooleanField(default=True, editable=False)),
                ('lexeme_relation', models.ForeignKey(to='wordengine.LexemeRelation', editable=False)),
                ('semantic_group_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.SemanticGroup')),
                ('semantic_group_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.SemanticGroup')),
                ('source', models.ManyToManyField(to='wordengine.Source', null=True, blank=True)),
                ('translation_based', models.ManyToManyField(related_name='translation_based_rel_+', to='wordengine.Translation', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsageConstraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wordform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('spelling', models.CharField(max_length=512)),
                ('dialect_multi', models.ManyToManyField(to='wordengine.Dialect', null=True, blank=True)),
                ('gramm_category_set', models.ForeignKey(to='wordengine.GrammCategorySet', null=True, blank=True)),
                ('lexeme', models.ForeignKey(to='wordengine.Lexeme', editable=False)),
                ('source', models.ManyToManyField(to='wordengine.Source', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordformSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('spelling', models.CharField(max_length=512)),
                ('informant', models.CharField(max_length=256)),
                ('gramm_category_set', models.ForeignKey(to='wordengine.GrammCategorySet', null=True, blank=True)),
                ('lexeme', models.ForeignKey(to='wordengine.Lexeme', editable=False)),
                ('source', models.ManyToManyField(to='wordengine.Source', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WritingSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('language', models.ForeignKey(to='wordengine.Language', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WritingSystemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='writingsystem',
            name='writing_system_type',
            field=models.ForeignKey(to='wordengine.WritingSystemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordformsample',
            name='writing_system',
            field=models.ForeignKey(to='wordengine.WritingSystem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordform',
            name='writing_system',
            field=models.ForeignKey(to='wordengine.WritingSystem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='translation',
            name='wordform_1',
            field=models.ForeignKey(related_name='translation_fst_set', to='wordengine.Wordform', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='translation',
            name='wordform_2',
            field=models.ForeignKey(related_name='translation_snd_set', to='wordengine.Wordform', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='source_type',
            field=models.ForeignKey(to='wordengine.SourceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='source',
            field=models.ManyToManyField(to='wordengine.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='theme',
            field=models.ManyToManyField(to='wordengine.Theme', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='usage_constraint_multi',
            field=models.ManyToManyField(to='wordengine.UsageConstraint', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lexemeproject',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lexeme',
            name='syntactic_category',
            field=models.ForeignKey(to='wordengine.SyntacticCategory', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='language',
            name='syntactic_category_multi',
            field=models.ManyToManyField(to='wordengine.SyntacticCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inflection',
            name='language',
            field=models.ForeignKey(to='wordengine.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inflection',
            name='syntactic_category_set',
            field=models.ForeignKey(to='wordengine.SyntacticCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grammcategoryset',
            name='language',
            field=models.ForeignKey(to='wordengine.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grammcategoryset',
            name='syntactic_category',
            field=models.ForeignKey(to='wordengine.SyntacticCategory'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grammcategoryset',
            unique_together=set([('language', 'position')]),
        ),
        migrations.AddField(
            model_name='grammcategory',
            name='gramm_category_type',
            field=models.ForeignKey(to='wordengine.GrammCategoryType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dialect',
            name='language',
            field=models.ForeignKey(to='wordengine.Language', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dialect',
            name='parent_dialect',
            field=models.ForeignKey(to='wordengine.Dialect', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columndata',
            name='language',
            field=models.ForeignKey(to='wordengine.Language', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columndata',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
    ]
