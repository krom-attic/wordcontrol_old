# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0007_auto_20141003_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectwordformliteral',
            name='col',
            field=models.ForeignKey(to='wordengine.ProjectColumnLiteral', blank=True, null=True),
            preserve_default=True,
        ),
    ]
