# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0037_auto_20141114_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lexemeparameter',
            options={},
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='term_id',
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='term_type',
        ),
    ]
