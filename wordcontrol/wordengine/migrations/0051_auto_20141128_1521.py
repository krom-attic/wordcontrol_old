# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0050_language_syntactic_category_m'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcWordform',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('spelling', models.CharField(max_length=512)),
                ('wordform', models.ForeignKey(to='wordengine.Wordform')),
                ('writing_system', models.ForeignKey(to='wordengine.WritingSystem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dictsemanticgroup',
            name='processing',
        ),
        migrations.RemoveField(
            model_name='dicttranslation',
            name='processing',
        ),
        migrations.RemoveField(
            model_name='dictwordform',
            name='processing',
        ),
        migrations.DeleteModel(
            name='Processing',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_comment',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_l',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='processing_type',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='source_l',
        ),
        migrations.RemoveField(
            model_name='projectsemanticgroup',
            name='col',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='wordform_1',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='wordform_2',
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='col',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='row',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
