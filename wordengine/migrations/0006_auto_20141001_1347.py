# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0005_auto_20141001_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='bind_wf_1',
            field=models.ForeignKey(related_name='translation_fst_set', default=0, to='wordengine.ProjectWordformLiteral'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='bind_wf_2',
            field=models.ForeignKey(related_name='translation_snd_set', default=0, to='wordengine.ProjectWordformLiteral'),
            preserve_default=False,
        ),
    ]
