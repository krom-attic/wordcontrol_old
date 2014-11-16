# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0039_auto_20141115_0113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lexeme',
            old_name='relations',
            new_name='lexeme_relation_m',
        ),
        migrations.RenameField(
            model_name='lexeme',
            old_name='translations',
            new_name='translation_m',
        ),
    ]
