# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0046_projectsemanticgroup_col'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projecttranslation',
            old_name='bind_wf_1',
            new_name='wordform_1',
        ),
        migrations.RenameField(
            model_name='projecttranslation',
            old_name='bind_wf_2',
            new_name='wordform_2',
        ),
    ]
