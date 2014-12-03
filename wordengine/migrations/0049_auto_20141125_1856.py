# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0048_auto_20141125_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyntCatsInLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('language', models.ForeignKey(to='wordengine.Language')),
                ('main_gramm_category_set', models.ForeignKey(to='wordengine.GrammCategorySet', blank=True, null=True)),
                ('syntactic_category', models.ForeignKey(to='wordengine.SyntacticCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='language',
            name='syntactic_category_m',
        ),
    ]
