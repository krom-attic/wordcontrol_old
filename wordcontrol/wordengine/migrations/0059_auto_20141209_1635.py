# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0058_auto_20141205_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='writingsystem',
            old_name='writing_system_type',
            new_name='writing_type',
        ),
        migrations.AddField(
            model_name='wordform',
            name='writing_type',
            field=models.CharField(default='PL', choices=[('PS', 'Phonetic strict'), ('PL', 'Phonetic loose'), ('O', 'Orthographic')], max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dialect',
            name='language',
            field=models.ForeignKey(to='wordengine.Language', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='source',
            name='language',
            field=models.ForeignKey(to='wordengine.Language', default=0),
            preserve_default=False,
        ),
    ]
