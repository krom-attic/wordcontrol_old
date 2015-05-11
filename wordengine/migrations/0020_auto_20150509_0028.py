# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0019_lexemeentry_mainform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='caption',
            field=models.CharField(default='', max_length=128, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='type',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'User'), ('D', 'Digitized'), ('P', 'Public')]),
        ),
        migrations.AlterUniqueTogether(
            name='grammcategory',
            unique_together=set([('gramm_category_type', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='wsindict',
            unique_together=set([('dictionary', 'writing_system'), ('dictionary', 'order')]),
        ),
    ]
