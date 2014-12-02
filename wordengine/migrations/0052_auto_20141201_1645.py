# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0051_auto_20141128_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectProcWordform',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('state', models.CharField(choices=[('N', 'New'), ('P', 'Processed')], max_length=2)),
                ('spelling', models.CharField(max_length=256)),
                ('col', models.ForeignKey(to='wordengine.ProjectColumn')),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('result', models.ForeignKey(null=True, blank=True, to='wordengine.Wordform')),
                ('wordform', models.ForeignKey(to='wordengine.ProjectWordform')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='col',
            field=models.ForeignKey(default=0, to='wordengine.ProjectColumn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='col',
            field=models.ForeignKey(default=0, to='wordengine.ProjectColumn'),
            preserve_default=False,
        ),
    ]
