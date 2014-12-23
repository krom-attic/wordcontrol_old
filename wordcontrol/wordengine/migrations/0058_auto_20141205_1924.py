# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0057_auto_20141205_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordformspell',
            old_name='original_wf',
            new_name='is_processed',
        ),
        migrations.AlterField(
            model_name='projectwordformspell',
            name='result',
            field=models.ForeignKey(to='wordengine.WordformSpell', default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectwordformspell',
            name='wordform',
            field=models.ForeignKey(to='wordengine.ProjectWordform', default=0),
            preserve_default=False,
        ),
    ]
