# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0013_auto_20141006_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='semanticgroup',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='processing_type',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='processing_type',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordform',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordform',
            name='processing_type',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordformsample',
            name='processing_comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordformsample',
            name='processing_type',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
