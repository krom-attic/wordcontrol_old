# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0049_auto_20141125_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='syntactic_category_m',
            field=models.ManyToManyField(null=True, through='wordengine.SyntCatsInLanguage', to='wordengine.SyntacticCategory', blank=True, related_name='synt_cat_set'),
            preserve_default=True,
        ),
    ]
