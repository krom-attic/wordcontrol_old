# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0007_auto_20150319_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='language',
            field=models.ForeignKey(to='wordengine.Language', default=1),
            preserve_default=False,
        ),
    ]
