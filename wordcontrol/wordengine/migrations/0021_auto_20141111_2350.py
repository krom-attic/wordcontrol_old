# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0020_auto_20141111_1800'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'src_field')]),
        ),
        migrations.RemoveField(
            model_name='projectdictionary',
            name='src_type',
        ),
    ]
