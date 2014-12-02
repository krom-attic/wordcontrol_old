# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0054_auto_20141202_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectprocwordform',
            name='result',
            field=models.ForeignKey(to='wordengine.ProcWordform', null=True, blank=True),
            preserve_default=True,
        ),
    ]
