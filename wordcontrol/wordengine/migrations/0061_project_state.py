# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0060_auto_20141225_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2, default='N'),
            preserve_default=False,
        ),
    ]
