# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0030_lexeme_lexeme_parameter_m'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectdictionary',
            unique_together=set([('value', 'src_obj', 'src_field', 'project')]),
        ),
    ]
