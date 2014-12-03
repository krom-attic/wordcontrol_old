# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0052_auto_20141201_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectdictionary',
            name='src_field',
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='params',
            field=models.CharField(blank=True, null=True, max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='dialect',
            field=models.CharField(blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='params',
            field=models.CharField(blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='params',
            field=models.CharField(blank=True, null=True, max_length=512),
            preserve_default=True,
        ),
    ]
