# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wordengine.models_ext_project


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0003_auto_20150304_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVCell',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projectcsvcell',),
        ),
        migrations.CreateModel(
            name='ProjectFromCSV',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.project',),
        ),
        migrations.CreateModel(
            name='ProjectLexemeProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projectlexeme', wordengine.models_ext_project.ProjectedModelMixIn),
        ),
        migrations.CreateModel(
            name='ProjectSemanticGroupProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projectsemanticgroup', wordengine.models_ext_project.ProjectedModelMixIn),
        ),
        migrations.CreateModel(
            name='ProjectTranslationProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projecttranslation', wordengine.models_ext_project.ProjectedModelMixIn),
        ),
        migrations.CreateModel(
            name='ProjectWordformProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projectwordform', wordengine.models_ext_project.ProjectedModelMixIn),
        ),
        migrations.CreateModel(
            name='ProjectWordformSpellProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('wordengine.projectwordformspell', wordengine.models_ext_project.ProjectedModelMixIn),
        ),
        migrations.AlterField(
            model_name='imgdata',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='project',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectcolumn',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projecttranslation',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='projectwordformspell',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='rawtextdata',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
        migrations.AlterField(
            model_name='srcimg',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
        ),
    ]
