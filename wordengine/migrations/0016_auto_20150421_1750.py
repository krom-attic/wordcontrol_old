# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0015_auto_20150420_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordformspelling',
            name='comment',
        ),
        migrations.AlterUniqueTogether(
            name='grammcategoryset',
            unique_together=set([('language', 'abbr_name'), ('language', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='wsindict',
            unique_together=set([('dictionary', 'order')]),
        ),
    ]
