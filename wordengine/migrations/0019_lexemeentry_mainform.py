# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0018_auto_20150428_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='mainform',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
