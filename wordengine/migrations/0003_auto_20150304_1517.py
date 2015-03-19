# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0002_auto_20150303_1203'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CSVCell',
            new_name='ProjectCSVCell',
        ),
    ]
