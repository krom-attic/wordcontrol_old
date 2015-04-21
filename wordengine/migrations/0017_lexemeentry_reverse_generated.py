# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0016_auto_20150421_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='reverse_generated',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=False,
        ),
    ]
