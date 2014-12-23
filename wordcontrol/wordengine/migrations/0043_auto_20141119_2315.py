# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0042_auto_20141116_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictSemanticGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('semantic_group', models.ForeignKey(to='wordengine.SemanticGroup')),
                ('source', models.ForeignKey(to='wordengine.Source', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DictTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('source', models.ForeignKey(to='wordengine.Source', blank=True, null=True)),
                ('translation', models.ForeignKey(to='wordengine.Translation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DictWordform',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('source', models.ForeignKey(to='wordengine.Source', blank=True, null=True)),
                ('wordform', models.ForeignKey(to='wordengine.Wordform')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='gramm_category_set',
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='lexeme',
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='source_m',
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='writing_system',
        ),
        migrations.DeleteModel(
            name='WordformSample',
        ),
        migrations.RenameField(
            model_name='inflection',
            old_name='syntactic_category_set',
            new_name='syntactic_category',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='source_m',
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
            name='source',
            field=models.ManyToManyField(to='wordengine.Source', through='wordengine.DictTranslation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordform',
            name='source',
            field=models.ManyToManyField(to='wordengine.Source', through='wordengine.DictWordform'),
            preserve_default=True,
        ),
    ]
