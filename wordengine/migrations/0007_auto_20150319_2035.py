# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0006_auto_20150319_2034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lexemeentry',
            old_name='sources',
            new_name='sources_text',
        ),
    ]
