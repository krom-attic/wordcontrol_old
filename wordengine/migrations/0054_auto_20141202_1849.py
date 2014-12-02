# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0053_auto_20141202_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcolumn',
            name='dialect_l',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectcolumn',
            name='writing_system_l',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='term_type',
            field=models.CharField(blank=True, default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='params',
            field=models.CharField(blank=True, default='', max_length=512),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='dialect',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='params',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='params',
            field=models.CharField(blank=True, default='', max_length=512),
            preserve_default=False,
        ),
    ]
