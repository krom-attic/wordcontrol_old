# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0020_auto_20150509_0028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lexemeentry',
            options={'permissions': (('edit_dict_data', 'Can add/update/delete lexeme entries in a given dictionary'),)},
        ),
    ]
