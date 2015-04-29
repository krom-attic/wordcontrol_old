# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordengine', '0010_auto_20150324_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='WSInDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order', models.SmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='dictionary',
            name='caption',
            field=models.CharField(null=True, blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='maintainer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dictionary',
            name='type',
            field=models.CharField(choices=[('U', 'User'), ('D', 'Digitized'), ('P', 'Public')], default='U', max_length=1),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='dictionary',
            name='writing_systems',
        ),
        migrations.AddField(
            model_name='wsindict',
            name='dictionary',
            field=models.ForeignKey(to='wordengine.Dictionary'),
        ),
        migrations.AddField(
            model_name='wsindict',
            name='writing_system',
            field=models.ForeignKey(to='wordengine.WritingSystem'),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='writing_systems',
            field=models.ManyToManyField(to='wordengine.WritingSystem', through='wordengine.WSInDict'),
        ),
    ]
