# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0001_squashed_0061_project_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvcell',
            old_name='col',
            new_name='colnum',
        ),
        migrations.RenameField(
            model_name='csvcell',
            old_name='row',
            new_name='rownum',
        ),
        migrations.AlterField(
            model_name='csvcell',
            name='project',
            field=models.ForeignKey(to='wordengine.Project'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dictchange',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dictsemanticgroup',
            name='source',
            field=models.ForeignKey(to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dicttranslation',
            name='source',
            field=models.ForeignKey(to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dictwordform',
            name='source',
            field=models.ForeignKey(to='wordengine.Source'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fieldchange',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grammcategorytype',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='filename',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='timestamp_upload',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='user_uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectwordformspell',
            name='wordform',
            field=models.ForeignKey(to='wordengine.ProjectWordform'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='syntacticcategory',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usageconstraint',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
