# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0006_auto_20141001_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRelation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('lexeme_1', models.ForeignKey(to='wordengine.ProjectLexeme', related_name='translation_fst_set')),
                ('lexeme_2', models.ForeignKey(to='wordengine.ProjectLexeme', related_name='translation_snd_set')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSemanticGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('dialect_multi', models.ManyToManyField(blank=True, to='wordengine.Dialect', null=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('theme', models.ForeignKey(to='wordengine.Theme', blank=True, null=True)),
                ('usage_constraint_multi', models.ManyToManyField(blank=True, to='wordengine.UsageConstraint', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSemanticGroupLiteral',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('params', models.CharField(blank=True, max_length=256)),
                ('dialect', models.CharField(blank=True, max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='dialect_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='dialect_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='theme',
        ),
        migrations.DeleteModel(
            name='ProjectTranslation',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='default_dialect',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='comment_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='comment_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='dialect_2',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='params',
        ),
        migrations.AddField(
            model_name='csvcell',
            name='project',
            field=models.ForeignKey(to='wordengine.Project', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='filename',
            field=models.CharField(default='Unknown', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='dialect',
            field=models.CharField(blank=True, max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='literal_value',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='num',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectlexemeliteral',
            name='col',
            field=models.ForeignKey(to='wordengine.ProjectColumnLiteral', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='direction',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='semantic_group_1',
            field=models.ForeignKey(default=0, to='wordengine.ProjectSemanticGroupLiteral', related_name='translation_fst_set'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='semantic_group_2',
            field=models.ForeignKey(default=0, to='wordengine.ProjectSemanticGroupLiteral', related_name='translation_snd_set'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='col',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='language',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='source',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='writing_system',
            field=models.CharField(max_length=256),
        ),
    ]
