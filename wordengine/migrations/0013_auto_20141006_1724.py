# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0012_auto_20141003_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcolumn',
            old_name='default_dialect',
            new_name='dialect',
        ),
        migrations.AddField(
            model_name='projectcolumn',
            name='literal',
            field=models.ForeignKey(to='wordengine.ProjectColumnLiteral', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='language',
            name='syntactic_category_multi',
            field=models.ManyToManyField(blank=True, null=True, to='wordengine.SyntacticCategory'),
        ),
    ]
