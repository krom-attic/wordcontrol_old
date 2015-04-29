# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0012_auto_20150417_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordformspelling',
            old_name='dialect',
            new_name='dialects',
        ),
        migrations.AddField(
            model_name='grammcategoryset',
            name='abbr_name',
            field=models.CharField(max_length=32, default='', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordformspelling',
            name='writing_system',
            field=models.ForeignKey(default=0, to='wordengine.WritingSystem', editable=False),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='dialect',
            unique_together=set([('term_abbr', 'language')]),
        ),
    ]
