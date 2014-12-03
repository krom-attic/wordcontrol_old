# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0011_remove_projectcolumnliteral_literal_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='source',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='writing_system',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
