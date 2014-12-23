# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0015_projectcolumnliteral_processing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semanticgroup',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='semanticgroup',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='wordformsample',
            name='processing_type',
        ),
        migrations.AddField(
            model_name='projectcolumn',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumn',
            name='processing_type',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='processing_type',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='source_parent',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.Source'),
            preserve_default=True,
        ),
    ]
