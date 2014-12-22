# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('wordengine', '0033_auto_20141114_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdictionary',
            name='content_type',
            field=models.ForeignKey(null=True, blank=True, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectdictionary',
            name='object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
