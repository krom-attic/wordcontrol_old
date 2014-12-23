# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0019_auto_20141111_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdictionary',
            name='src_field',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdictionary',
            name='src_obj',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
