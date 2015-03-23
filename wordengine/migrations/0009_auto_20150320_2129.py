# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0008_lexemeentry_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='index',
            field=models.CharField(db_index=True, max_length=256, default=''),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='lexemeentry',
            unique_together=set([('language', 'index')]),
        ),
    ]
