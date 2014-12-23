# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0003_auto_20140919_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlexemeliteral',
            name='params',
            field=models.CharField(max_length=512, blank=True),
        ),
    ]
