# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0036_auto_20141114_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lexeme',
            options={},
        ),
        migrations.AlterModelOptions(
            name='lexemeparameter',
            options={'verbose_name': 'Lexemea'},
        ),
    ]
