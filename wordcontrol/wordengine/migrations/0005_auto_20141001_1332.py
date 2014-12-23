# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordengine', '0004_auto_20140919_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVCell',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('value', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='projecttranslationliteral',
            old_name='dialect_1',
            new_name='params',
        ),
        migrations.RenameField(
            model_name='projectwordform',
            old_name='wordform',
            new_name='spelling',
        ),
        migrations.RenameField(
            model_name='projectwordformliteral',
            old_name='wordform',
            new_name='spelling',
        ),
        migrations.RemoveField(
            model_name='projectcolumn',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projectcolumnliteral',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projectlexeme',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projectlexemeliteral',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projecttranslation',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projecttranslationliteral',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='projectwordform',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='col_num',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='dialect',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='gramm_category_set',
        ),
        migrations.RemoveField(
            model_name='projectwordformliteral',
            name='informant',
        ),
        migrations.AddField(
            model_name='project',
            name='timestamp_upload',
            field=models.DateTimeField(default=datetime.date.today(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='user_uploader',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumn',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectcolumnliteral',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectlexeme',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectlexemeliteral',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttranslation',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttranslationliteral',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwordform',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwordformliteral',
            name='csvcell',
            field=models.ForeignKey(default=0, to='wordengine.CSVCell'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwordformliteral',
            name='params',
            field=models.CharField(default=0, max_length=512, blank=True),
            preserve_default=False,
        ),
    ]
