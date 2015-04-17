# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0011_auto_20150324_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordformSpelling',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('spelling', models.CharField(editable=False, max_length=512)),
                ('comment', models.TextField(blank=True, editable=False)),
                ('dialect', models.ManyToManyField(null=True, blank=True, to='wordengine.Dialect', editable=False)),
                ('gramm_category_set', models.ForeignKey(editable=False, null=True, blank=True, to='wordengine.GrammCategorySet')),
            ],
        ),
        migrations.AlterField(
            model_name='lexemeentry',
            name='dictionary',
            field=models.ForeignKey(to='wordengine.Dictionary', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lexemeentry',
            name='forms_text',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='wordformspelling',
            name='lexeme_entry',
            field=models.ForeignKey(to='wordengine.LexemeEntry', editable=False),
        ),
    ]
