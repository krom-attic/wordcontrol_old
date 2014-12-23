# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0017_auto_20141104_1738'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_type')]),
        ),
    ]
