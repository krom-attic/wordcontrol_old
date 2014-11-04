# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0016_auto_20141006_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('x', models.SmallIntegerField()),
                ('y', models.SmallIntegerField()),
                ('h', models.SmallIntegerField()),
                ('w', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectDictionary',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('value', models.CharField(max_length=256)),
                ('src_type', models.CharField(max_length=256)),
                ('term_type', models.CharField(max_length=128)),
                ('term_id', models.PositiveIntegerField(null=True, blank=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawTextData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('text', models.TextField(blank=True)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SrcImg',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('state', models.SmallIntegerField()),
                ('filename', models.CharField(max_length=256)),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='imgdata',
            name='img',
            field=models.ForeignKey(to='wordengine.SrcImg'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imgdata',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imgdata',
            name='text',
            field=models.ForeignKey(to='wordengine.RawTextData'),
            preserve_default=True,
        ),
    ]
