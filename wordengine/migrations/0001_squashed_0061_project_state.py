# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialect',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp_change', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('timestamp_review', models.DateTimeField(null=True, blank=True, editable=False)),
                ('user_changer', models.ForeignKey(related_name='wordengine_dictchange_changer', to=settings.AUTH_USER_MODEL, editable=False)),
                ('user_reviewer', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False)),
                ('content_type', models.ForeignKey(default=0, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldChange',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp_change', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('field_name', models.CharField(max_length=256)),
                ('old_value', models.CharField(max_length=512, blank=True)),
                ('new_value', models.CharField(max_length=512, blank=True)),
                ('user_changer', models.ForeignKey(related_name='wordengine_fieldchange_changer', to=settings.AUTH_USER_MODEL, editable=False)),
                ('content_type', models.ForeignKey(default=0, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inflection',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('inflection', models.ForeignKey(null=True, blank=True, to='wordengine.Inflection')),
                ('language', models.ForeignKey(to='wordengine.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LexemeRelation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('lexeme_1', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_fst_set')),
                ('lexeme_2', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_snd_set')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp_upload', models.DateTimeField(default=datetime.date(2015, 3, 1), auto_now_add=True)),
                ('user_uploader', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL, editable=False)),
                ('filename', models.CharField(default='Unknown', max_length=512)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SemanticGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('dialect_multi', models.ManyToManyField(null=True, to='wordengine.Dialect', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('language', models.ForeignKey(null=True, blank=True, to='wordengine.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SyntacticCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslatedTerm',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('direction', models.PositiveSmallIntegerField()),
                ('is_visible', models.BooleanField(default=True, editable=False)),
                ('lexeme_relation', models.ForeignKey(to='wordengine.LexemeRelation', editable=False)),
                ('semantic_group_1', models.ForeignKey(to='wordengine.SemanticGroup', related_name='translation_fst_set')),
                ('semantic_group_2', models.ForeignKey(to='wordengine.SemanticGroup', related_name='translation_snd_set')),
                ('source', models.ManyToManyField(null=True, to='wordengine.Source', blank=True)),
                ('translation_based', models.ManyToManyField(null=True, related_name='translation_based_rel_+', to='wordengine.Translation', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsageConstraint',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wordform',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('spelling', models.CharField(max_length=512)),
                ('dialect_multi', models.ManyToManyField(null=True, to='wordengine.Dialect', blank=True)),
                ('gramm_category_set', models.ForeignKey(null=True, blank=True, to='wordengine.GrammCategorySet')),
                ('lexeme', models.ForeignKey(to='wordengine.Lexeme', editable=False)),
                ('source', models.ManyToManyField(null=True, to='wordengine.Source', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WritingSystem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('language', models.ForeignKey(null=True, blank=True, to='wordengine.Language')),
                ('writing_system_type', models.CharField(choices=[('PS', 'Phonetic strict'), ('PL', 'Phonetic loose'), ('O', 'Orthographic')], max_length=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
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
            field=models.ForeignKey(null=True, blank=True, related_name='translation_fst_set', to='wordengine.Wordform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='translation',
            name='wordform_2',
            field=models.ForeignKey(null=True, blank=True, related_name='translation_snd_set', to='wordengine.Wordform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='source_type',
            field=models.CharField(choices=[('OK', 'Own knowledge'), ('DT', 'Dictionary/Textbook'), ('SP', 'Scientific publication'), ('FA', 'Field archive'), ('OT', 'Other trustworthy source')], max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='source_m',
            field=models.ManyToManyField(null=True, to='wordengine.Source', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='theme_m',
            field=models.ManyToManyField(null=True, to='wordengine.Theme', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='usage_constraint_m',
            field=models.ManyToManyField(null=True, to='wordengine.UsageConstraint', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lexeme',
            name='syntactic_category',
            field=models.ForeignKey(to='wordengine.SyntacticCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='language',
            name='syntactic_category_m',
            field=models.ManyToManyField(null=True, to='wordengine.SyntacticCategory', blank=True),
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
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dialect',
            name='parent_dialect',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Dialect'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
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
        migrations.RemoveField(
            model_name='translation',
            name='translation_based',
        ),
        migrations.AddField(
            model_name='dialect',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grammcategory',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='language',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='language',
            name='iso_code',
            field=models.CharField(default='zzz', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lexemerelation',
            name='relation_type',
            field=models.CharField(choices=[('TR', 'Translation')], max_length=2),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CSVCell',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('row', models.IntegerField()),
                ('col', models.SmallIntegerField()),
                ('value', models.TextField(blank=True)),
                ('project', models.ForeignKey(default=0, to='wordengine.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
            name='processing_comment',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='processing_type',
            field=models.CharField(choices=[('NP', 'No processing'), ('WS', 'Writing system changed')], max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='source_parent',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ImgData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('x', models.SmallIntegerField()),
                ('y', models.SmallIntegerField()),
                ('h', models.SmallIntegerField()),
                ('w', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectDictionary',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.SmallIntegerField()),
                ('value', models.CharField(max_length=256)),
                ('src_type', models.CharField(max_length=256)),
                ('term_type', models.CharField(max_length=128)),
                ('term_id', models.PositiveIntegerField(null=True, blank=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawTextData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('text', models.TextField(blank=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SrcImg',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('filename', models.CharField(max_length=256)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='imgdata',
            name='img',
            field=models.ForeignKey(to='wordengine.SrcImg'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imgdata',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imgdata',
            name='text',
            field=models.ForeignKey(to='wordengine.RawTextData'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_type')]),
        ),
        migrations.AlterField(
            model_name='imgdata',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectdictionary',
            name='src_field',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdictionary',
            name='src_obj',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'src_field')]),
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='src_type',
        ),
        migrations.RenameField(
            model_name='grammcategoryset',
            old_name='gramm_category_multi',
            new_name='gramm_category_m',
        ),
        migrations.RenameField(
            model_name='semanticgroup',
            old_name='dialect_multi',
            new_name='dialect_m',
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
        migrations.CreateModel(
            name='ProjectColumn',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('language_l', models.CharField(max_length=256)),
                ('dialect_l', models.CharField(null=True, max_length=256, blank=True)),
                ('source_l', models.CharField(null=True, max_length=256, blank=True)),
                ('writing_system_l', models.CharField(null=True, max_length=256, blank=True)),
                ('processing_l', models.CharField(null=True, max_length=256, blank=True)),
                ('num', models.SmallIntegerField()),
                ('processing_type', models.CharField(null=True, choices=[('NP', 'No processing'), ('WS', 'Writing system changed')], max_length=2, blank=True)),
                ('processing_comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect', models.ForeignKey(null=True, blank=True, to='wordengine.Dialect')),
                ('language', models.ForeignKey(null=True, blank=True, to='wordengine.Language')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('source', models.ForeignKey(null=True, blank=True, to='wordengine.Source')),
                ('writing_system', models.ForeignKey(null=True, blank=True, to='wordengine.WritingSystem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLexeme',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('syntactic_category_l', models.CharField(max_length=256)),
                ('params_l', models.CharField(max_length=512, blank=True)),
                ('col', models.ForeignKey(null=True, blank=True, to='wordengine.ProjectColumn')),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('inflection', models.ForeignKey(null=True, blank=True, to='wordengine.Inflection')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('syntactic_category', models.ForeignKey(null=True, blank=True, to='wordengine.SyntacticCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSemanticGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('params_l', models.CharField(max_length=256, blank=True)),
                ('dialect_l', models.CharField(max_length=256, blank=True)),
                ('comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect_m', models.ManyToManyField(null=True, to='wordengine.Dialect', blank=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('theme', models.ForeignKey(null=True, blank=True, to='wordengine.Theme')),
                ('usage_constraint_m', models.ManyToManyField(null=True, to='wordengine.UsageConstraint', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWordform',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('spelling', models.CharField(max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('params', models.CharField(max_length=512, blank=True)),
                ('col', models.ForeignKey(null=True, blank=True, to='wordengine.ProjectColumn')),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('lexeme', models.ForeignKey(to='wordengine.ProjectLexeme')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('direction', models.CharField(choices=[('F', 'Forward'), ('B', 'Backward'), ('D', 'Duplex')], max_length=1)),
                ('relation_type', models.CharField(max_length=32)),
                ('lexeme_1', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_fst_set')),
                ('lexeme_2', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_snd_set')),
                ('wordform_1', models.ForeignKey(null=True, blank=True, related_name='relation_fst_set', to='wordengine.Wordform')),
                ('wordform_2', models.ForeignKey(null=True, blank=True, related_name='relation_snd_set', to='wordengine.Wordform')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='lexemerelation',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='lexemerelation',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='is_visible',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='lexeme_relation',
        ),
        migrations.DeleteModel(
            name='LexemeRelation',
        ),
        migrations.AddField(
            model_name='lexeme',
            name='relations',
            field=models.ManyToManyField(null=True, related_name='relation_set', to='wordengine.Lexeme', through='wordengine.Relation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lexeme',
            name='translations',
            field=models.ManyToManyField(null=True, related_name='translation_set', to='wordengine.Lexeme', through='wordengine.Translation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='translation',
            name='lexeme_1',
            field=models.ForeignKey(default=0, related_name='translation_fst_set', to='wordengine.Lexeme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='lexeme_2',
            field=models.ForeignKey(default=0, related_name='translation_snd_set', to='wordengine.Lexeme'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='translation',
            name='direction',
            field=models.CharField(choices=[('F', 'Forward'), ('B', 'Backward'), ('D', 'Duplex')], max_length=1),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LexemeParameter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('direction', models.SmallIntegerField()),
                ('lexeme_1', models.ForeignKey(to='wordengine.ProjectLexeme', related_name='translation_fst_set')),
                ('lexeme_2', models.ForeignKey(to='wordengine.ProjectLexeme', related_name='translation_snd_set')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('semantic_group_1', models.ForeignKey(to='wordengine.ProjectSemanticGroup', related_name='translation_fst_set')),
                ('semantic_group_2', models.ForeignKey(to='wordengine.ProjectSemanticGroup', related_name='translation_snd_set')),
                ('result', models.ForeignKey(null=True, blank=True, to='wordengine.Translation')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lexeme',
            name='lexeme_parameter_m',
            field=models.ManyToManyField(null=True, to='wordengine.LexemeParameter', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'src_field', 'project')]),
        ),
        migrations.RenameField(
            model_name='projectsemanticgroup',
            old_name='theme',
            new_name='theme_r',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='inflection',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='syntactic_category',
        ),
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
        migrations.AlterModelOptions(
            name='lexeme',
            options={'verbose_name': 'Lexeme'},
        ),
        migrations.AlterModelOptions(
            name='lexeme',
            options={'verbose_name': 'Lexemea'},
        ),
        migrations.AlterModelOptions(
            name='lexeme',
            options={},
        ),
        migrations.AlterModelOptions(
            name='lexemeparameter',
            options={'verbose_name': 'Lexemea'},
        ),
        migrations.AlterModelOptions(
            name='lexemeparameter',
            options={},
        ),
        migrations.RenameField(
            model_name='lexeme',
            old_name='relations',
            new_name='lexeme_relation_m',
        ),
        migrations.RenameField(
            model_name='lexeme',
            old_name='translations',
            new_name='translation_m',
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='term_type',
            field=models.CharField(null=True, max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectlexeme',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Lexeme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectsemanticgroup',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.SemanticGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordform',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Wordform'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DictSemanticGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('semantic_group', models.ForeignKey(to='wordengine.SemanticGroup')),
                ('source', models.ForeignKey(default=1, to='wordengine.Source')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DictTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('source', models.ForeignKey(default=1, to='wordengine.Source')),
                ('translation', models.ForeignKey(to='wordengine.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DictWordform',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('source', models.ForeignKey(default=1, to='wordengine.Source')),
                ('wordform', models.ForeignKey(to='wordengine.Wordform')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='inflection',
            old_name='syntactic_category_set',
            new_name='syntactic_category',
        ),
        migrations.RemoveField(
            model_name='semanticgroup',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='semanticgroup',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='semanticgroup',
            name='source_m',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='source_m',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='source_m',
        ),
        migrations.AddField(
            model_name='translation',
            name='source_m',
            field=models.ManyToManyField(through='wordengine.DictTranslation', to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordform',
            name='source_m',
            field=models.ManyToManyField(through='wordengine.DictWordform', to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='source_m',
            field=models.ManyToManyField(through='wordengine.DictSemanticGroup', to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='comment',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='src_field',
            field=models.CharField(null=True, max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'term_type', 'project')]),
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='source',
        ),
        migrations.RemoveField(
            model_name='source',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='source',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='source',
            name='source_parent',
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SyntCatsInLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('language', models.ForeignKey(to='wordengine.Language')),
                ('main_gramm_category_set', models.ForeignKey(null=True, blank=True, to='wordengine.GrammCategorySet')),
                ('syntactic_category', models.ForeignKey(to='wordengine.SyntacticCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='language',
            name='syntactic_category_m',
        ),
        migrations.AddField(
            model_name='language',
            name='syntactic_category_m',
            field=models.ManyToManyField(null=True, related_name='synt_cat_set', to='wordengine.SyntacticCategory', through='wordengine.SyntCatsInLanguage', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_l',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='source_l',
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='col',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='row',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='col',
            field=models.ForeignKey(default=0, to='wordengine.ProjectColumn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='col',
            field=models.ForeignKey(default=0, to='wordengine.ProjectColumn'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='src_field',
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='params',
            field=models.CharField(null=True, max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='dialect',
            field=models.CharField(null=True, max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='params',
            field=models.CharField(null=True, max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='params',
            field=models.CharField(null=True, max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcolumn',
            name='dialect_l',
            field=models.CharField(default='', max_length=256, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectcolumn',
            name='writing_system_l',
            field=models.CharField(default='', max_length=256, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='term_type',
            field=models.CharField(default='', max_length=128, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='params',
            field=models.CharField(default='', max_length=512, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='dialect',
            field=models.CharField(default='', max_length=256, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='params',
            field=models.CharField(default='', max_length=256, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='params',
            field=models.CharField(default='', max_length=512, blank=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ProjectWordformSpell',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('is_processed', models.BooleanField()),
                ('spelling', models.CharField(max_length=256)),
                ('col', models.ForeignKey(to='wordengine.ProjectColumn')),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordformSpell',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('spelling', models.CharField(max_length=512)),
                ('is_processed', models.BooleanField()),
                ('wordform', models.ForeignKey(to='wordengine.Wordform')),
                ('writing_system', models.ForeignKey(to='wordengine.WritingSystem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectwordformspell',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.WordformSpell'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordformspell',
            name='wordform',
            field=models.ForeignKey(default=0, to='wordengine.ProjectWordform'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='spelling',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='spelling',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='writing_system',
        ),
        migrations.RenameField(
            model_name='writingsystem',
            old_name='writing_system_type',
            new_name='writing_type',
        ),
        migrations.AddField(
            model_name='wordform',
            name='writing_type',
            field=models.CharField(default='PL', max_length=2, choices=[('PS', 'Phonetic strict'), ('PL', 'Phonetic loose'), ('O', 'Orthographic')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dialect',
            name='language',
            field=models.ForeignKey(default=0, to='wordengine.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='source',
            name='language',
            field=models.ForeignKey(default=0, to='wordengine.Language'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='state',
            field=models.CharField(default='N', max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
            preserve_default=False,
        ),
    ]
