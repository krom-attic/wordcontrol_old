# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0024_auto_20141112_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('comment', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(editable=False, default=False)),
                ('direction', models.CharField(choices=[('F', 'Forward'), ('B', 'Backward'), ('D', 'Duplex')], max_length=1)),
                ('relation_type', models.CharField(max_length=32)),
                ('lexeme_1', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_fst_set')),
                ('lexeme_2', models.ForeignKey(to='wordengine.Lexeme', related_name='relation_snd_set')),
                ('source_m', models.ManyToManyField(to='wordengine.Source', null=True, blank=True)),
                ('wordform_1', models.ForeignKey(blank=True, related_name='relation_fst_set', null=True, to='wordengine.Wordform')),
                ('wordform_2', models.ForeignKey(blank=True, related_name='relation_snd_set', null=True, to='wordengine.Wordform')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='lexemerelation',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='lexemerelation',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='is_visible',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='lexeme_relation',
        ),
        migrations.DeleteModel(
            name='LexemeRelation',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='translation_based_m',
        ),
        migrations.AddField(
            model_name='lexeme',
            name='relations',
            field=models.ManyToManyField(related_name='relation_set', null=True, through='wordengine.Relation', blank=True, to='wordengine.Lexeme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lexeme',
            name='translations',
            field=models.ManyToManyField(related_name='translation_set', null=True, through='wordengine.Translation', blank=True, to='wordengine.Lexeme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='translation',
            name='lexeme_1',
            field=models.ForeignKey(related_name='translation_fst_set', default=0, to='wordengine.Lexeme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='lexeme_2',
            field=models.ForeignKey(related_name='translation_snd_set', default=0, to='wordengine.Lexeme'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='translation',
            name='direction',
            field=models.CharField(choices=[('F', 'Forward'), ('B', 'Backward'), ('D', 'Duplex')], max_length=1),
        ),
    ]
