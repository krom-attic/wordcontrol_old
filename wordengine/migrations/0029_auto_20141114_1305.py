# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordengine', '0028_auto_20141113_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(max_length=2, choices=[('N', 'New'), ('P', 'Processed')])),
                ('direction', models.SmallIntegerField()),
                ('bind_wf_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectWordform')),
                ('bind_wf_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectWordform')),
                ('lexeme_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectLexeme')),
                ('lexeme_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectLexeme')),
                ('project', models.ForeignKey(to='wordengine.Project')),
                ('semantic_group_1', models.ForeignKey(related_name='translation_fst_set', to='wordengine.ProjectSemanticGroup')),
                ('semantic_group_2', models.ForeignKey(related_name='translation_snd_set', to='wordengine.ProjectSemanticGroup')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='bind_wf_1',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='bind_wf_2',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='lexeme_1',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='lexeme_2',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='semantic_group_1',
        ),
        migrations.RemoveField(
            model_name='projectrelation',
            name='semantic_group_2',
        ),
        migrations.DeleteModel(
            name='ProjectRelation',
        ),
    ]
