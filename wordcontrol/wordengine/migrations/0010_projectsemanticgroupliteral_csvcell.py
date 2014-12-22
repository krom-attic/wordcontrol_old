# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0009_auto_20141003_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsemanticgroupliteral',
            name='csvcell',
            field=models.ForeignKey(to='wordengine.CSVCell', default=0),
            preserve_default=False,
        ),
    ]
