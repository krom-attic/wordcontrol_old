# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0055_auto_20141202_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectWordformSpell',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('state', models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')])),
                ('is_processed', models.BooleanField()),
                ('spelling', models.CharField(max_length=256)),
                ('col', models.ForeignKey(to='wordengine.ProjectColumn')),
                ('csvcell', models.ForeignKey(to='wordengine.CSVCell')),
                ('project', models.ForeignKey(to='wordengine.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordformSpell',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('spelling', models.CharField(max_length=512)),
                ('original_wf', models.BooleanField()),
                ('wordform', models.ForeignKey(to='wordengine.Wordform')),
                ('writing_system', models.ForeignKey(to='wordengine.WritingSystem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='procwordform',
            name='wordform',
        ),
        migrations.RemoveField(
            model_name='procwordform',
            name='writing_system',
        ),
        migrations.RemoveField(
            model_name='projectprocwordform',
            name='col',
        ),
        migrations.RemoveField(
            model_name='projectprocwordform',
            name='csvcell',
        ),
        migrations.RemoveField(
            model_name='projectprocwordform',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectprocwordform',
            name='result',
        ),
        migrations.DeleteModel(
            name='ProcWordform',
        ),
        migrations.RemoveField(
            model_name='projectprocwordform',
            name='wordform',
        ),
        migrations.DeleteModel(
            name='ProjectProcWordform',
        ),
        migrations.AddField(
            model_name='projectwordformspell',
            name='result',
            field=models.ForeignKey(null=True, blank=True, to='wordengine.WordformSpell'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwordformspell',
            name='wordform',
            field=models.ForeignKey(to='wordengine.ProjectWordform'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='spelling',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='spelling',
        ),
        migrations.RemoveField(
            model_name='wordform',
            name='writing_system',
        ),
    ]
