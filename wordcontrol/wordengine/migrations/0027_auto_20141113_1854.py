# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('wordengine', '0026_lexemeparameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdictionary',
            name='content_type',
            field=models.ForeignKey(default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdictionary',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
