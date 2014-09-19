# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0002_auto_20140919_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='inflection',
        ),
        migrations.AddField(
            model_name='projectlexemeliteral',
            name='params',
            field=models.CharField(default='zzz', max_length=512),
            preserve_default=False,
        ),
    ]
