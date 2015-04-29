# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0014_auto_20150420_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='iso_code',
            field=models.CharField(max_length=8, db_index=True),
        ),
    ]
