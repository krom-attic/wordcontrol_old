# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0038_auto_20141114_2033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectdictionary',
            old_name='object_id',
            new_name='term_id',
        ),
        migrations.RenameField(
            model_name='projectdictionary',
            old_name='content_type',
            new_name='term_type',
        ),
    ]
