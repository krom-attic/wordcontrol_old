# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0044_auto_20141119_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictsemanticgroup',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='dicttranslation',
            name='comment',
        ),
        migrations.AddField(
            model_name='semanticgroup',
            name='comment',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='src_field',
            field=models.CharField(blank=True, max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'term_type', 'project')]),
        ),
    ]
