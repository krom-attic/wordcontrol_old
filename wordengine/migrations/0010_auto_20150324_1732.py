# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0009_auto_20150320_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('writing_systems', models.ForeignKey(to='wordengine.WritingSystem')),
            ],
        ),
        migrations.RemoveField(
            model_name='dictwordform',
            name='source',
        ),
        migrations.RemoveField(
            model_name='dictwordform',
            name='wordform',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='source_m',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='writing_type',
        ),
        migrations.RemoveField(
            model_name='wordformspell',
            name='is_processed',
        ),
        migrations.RemoveField(
            model_name='wordformspell',
            name='spelling',
        ),
        migrations.RemoveField(
            model_name='wordformspell',
            name='wordform',
        ),
        migrations.RemoveField(
            model_name='wordformspell',
            name='writing_system',
        ),
        migrations.AddField(
            model_name='lexemeentry',
            name='slug',
            field=models.SlugField(max_length=128, default='foo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordform',
            name='spelling',
            field=models.CharField(max_length=512, default='bar'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='lexemeentry',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='DictWordform',
        ),
        migrations.RemoveField(
            model_name='lexemeentry',
            name='index',
        ),
        migrations.AddField(
            model_name='lexemeentry',
            name='dictionary',
            field=models.ForeignKey(null=True, to='wordengine.Dictionary'),
        ),
        migrations.AddField(
            model_name='wordform',
            name='dictionary',
            field=models.ForeignKey(null=True, to='wordengine.Dictionary'),
        ),
    ]
