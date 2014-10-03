# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0008_projectwordformliteral_col'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcolumn',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='csvcell',
        ),
    ]
