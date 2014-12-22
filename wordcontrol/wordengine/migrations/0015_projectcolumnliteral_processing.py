# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0014_auto_20141006_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='processing',
            field=models.CharField(blank=True, max_length=256, null=True),
            preserve_default=True,
        ),
    ]
