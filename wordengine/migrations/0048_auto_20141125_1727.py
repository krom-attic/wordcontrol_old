# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0047_auto_20141125_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Processing',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('term_full', models.CharField(max_length=256)),
                ('term_abbr', models.CharField(max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('processing_type', models.CharField(max_length=2, choices=[('NP', 'No processing'), ('WS', 'Writing system changed')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
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
            model_name='dictsemanticgroup',
            name='processing',
            field=models.ForeignKey(to='wordengine.Processing', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dicttranslation',
            name='processing',
            field=models.ForeignKey(to='wordengine.Processing', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dictwordform',
            name='processing',
            field=models.ForeignKey(to='wordengine.Processing', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(to='wordengine.Source', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dictsemanticgroup',
            name='source',
            field=models.ForeignKey(default=1, to='wordengine.Source'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dicttranslation',
            name='source',
            field=models.ForeignKey(default=1, to='wordengine.Source'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dictwordform',
            name='source',
            field=models.ForeignKey(default=1, to='wordengine.Source'),
            preserve_default=False,
        ),
    ]
