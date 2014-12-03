# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0045_auto_20141125_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsemanticgroup',
            name='col',
            field=models.ForeignKey(blank=True, to='wordengine.ProjectColumn', null=True),
            preserve_default=True,
        ),
    ]
