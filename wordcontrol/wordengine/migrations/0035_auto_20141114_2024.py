# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0034_auto_20141114_1744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lexeme',
            options={'verbose_name': 'Lexeme'},
        ),
    ]
