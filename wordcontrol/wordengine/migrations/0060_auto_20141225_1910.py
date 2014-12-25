# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0059_auto_20141209_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectwordformspell',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.WordformSpell'),
            preserve_default=True,
        ),
    ]
