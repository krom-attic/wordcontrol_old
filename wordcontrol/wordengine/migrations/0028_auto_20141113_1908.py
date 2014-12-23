# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('wordengine', '0027_auto_20141113_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictchange',
            name='object_type',
        ),
        migrations.RemoveField(
            model_name='fieldchange',
            name='object_type',
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='object_id',
        ),
        migrations.AddField(
            model_name='dictchange',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fieldchange',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dictchange',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='fieldchange',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
