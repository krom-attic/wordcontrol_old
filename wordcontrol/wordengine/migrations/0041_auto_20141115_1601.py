# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0040_auto_20141115_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdictionary',
            name='term_type',
            field=models.CharField(blank=True, max_length=128, null=True),
            preserve_default=True,
        ),
    ]
