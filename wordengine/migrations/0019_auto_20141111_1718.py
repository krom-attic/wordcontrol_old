# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0018_auto_20141105_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectsemanticgroupliteral',
            name='dialect',
        ),
        migrations.AlterField(
            model_name='imgdata',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='lexemerelation',
            name='relation_type',
            field=models.CharField(max_length=2, choices=[('TR', 'Translation')]),
        ),
        migrations.AlterField(
            model_name='projectcolumn',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectcolumnliteral',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectdictionary',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectlexeme',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectlexemeliteral',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectrelation',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectsemanticgroup',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectsemanticgroupliteral',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projecttranslationliteral',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectwordform',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='projectwordformliteral',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='rawtextdata',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='source',
            name='processing_type',
            field=models.CharField(max_length=2, choices=[('NP', 'No processing'), ('WS', 'Writing system changed')]),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_type',
            field=models.CharField(max_length=2, choices=[('OK', 'Own knowledge'), ('DT', 'Dictionary/Textbook'), ('SP', 'Scientific publication'), ('FA', 'Field archive'), ('OT', 'Other trustworthy source')]),
        ),
        migrations.AlterField(
            model_name='srcimg',
            name='state',
            field=models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')]),
        ),
        migrations.AlterField(
            model_name='writingsystem',
            name='writing_system_type',
            field=models.CharField(max_length=2, choices=[('PS', 'Phonetic strict'), ('PL', 'Phonetic loose'), ('O', 'Orthographic')]),
        ),
    ]
