# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0017_lexemeentry_reverse_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='lexemeentry',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 4, 28, 15, 11, 50, 645046)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lexemeentry',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 4, 28, 15, 11, 55, 637546)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lexemeentry',
            name='disambig',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='lexemeentry',
            name='reverse_generated',
            field=models.BooleanField(editable=False, default=False),
        ),
    ]
