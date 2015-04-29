# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0004_auto_20150319_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='LexemeEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('forms_text', models.TextField(blank=True)),
                ('relations_text', models.TextField(blank=True)),
                ('translations_text', models.TextField(blank=True)),
                ('syntactic_category', models.ForeignKey(to='wordengine.SyntacticCategory')),
            ],
        ),
    ]
