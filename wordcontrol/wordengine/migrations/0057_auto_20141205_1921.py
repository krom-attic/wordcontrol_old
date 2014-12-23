# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0056_auto_20141205_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectwordformspell',
            name='wordform',
            field=models.ForeignKey(blank=True, to='wordengine.ProjectWordform', null=True),
            preserve_default=True,
        ),
    ]
