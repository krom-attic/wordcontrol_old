# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SyntacticCategory'
        db.create_table('wordengine_syntacticcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['SyntacticCategory'])

        # Adding model 'UsageConstraint'
        db.create_table('wordengine_usageconstraint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['UsageConstraint'])

        # Adding model 'GrammCategoryType'
        db.create_table('wordengine_grammcategorytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['GrammCategoryType'])

        # Adding model 'GrammCategory'
        db.create_table('wordengine_grammcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('gramm_category_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.GrammCategoryType'])),
            ('position', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('wordengine', ['GrammCategory'])

        # Adding model 'Language'
        db.create_table('wordengine_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['Language'])

        # Adding M2M table for field syntactic_category_multi on 'Language'
        m2m_table_name = db.shorten_name('wordengine_language_syntactic_category_multi')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('language', models.ForeignKey(orm['wordengine.language'], null=False)),
            ('syntacticcategory', models.ForeignKey(orm['wordengine.syntacticcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['language_id', 'syntacticcategory_id'])

        # Adding model 'SourceType'
        db.create_table('wordengine_sourcetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['SourceType'])

        # Adding model 'Source'
        db.create_table('wordengine_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.Language'], blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('source_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.SourceType'])),
        ))
        db.send_create_signal('wordengine', ['Source'])

        # Adding model 'DictChange'
        db.create_table('wordengine_dictchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_changer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wordengine_dictchange_changer', to=orm['auth.User'])),
            ('timestamp_change', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('object_type', self.gf('django.db.models.fields.TextField')(max_length=256)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_reviewer', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True)),
            ('timestamp_review', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('wordengine', ['DictChange'])

        # Adding model 'FieldChange'
        db.create_table('wordengine_fieldchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_changer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wordengine_fieldchange_changer', to=orm['auth.User'])),
            ('timestamp_change', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('object_type', self.gf('django.db.models.fields.TextField')(max_length=256)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('new_value', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('wordengine', ['FieldChange'])

        # Adding model 'Dialect'
        db.create_table('wordengine_dialect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.Language'], blank=True)),
            ('parent_dialect', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.Dialect'], blank=True)),
        ))
        db.send_create_signal('wordengine', ['Dialect'])

        # Adding model 'WritingSystemType'
        db.create_table('wordengine_writingsystemtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['WritingSystemType'])

        # Adding model 'WritingSystem'
        db.create_table('wordengine_writingsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_full', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.Language'], blank=True)),
            ('writing_system_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.WritingSystemType'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('wordengine', ['WritingSystem'])

        # Adding model 'GrammCategorySet'
        db.create_table('wordengine_grammcategoryset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Language'])),
            ('syntactic_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.SyntacticCategory'])),
            ('position', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('wordengine', ['GrammCategorySet'])

        # Adding unique constraint on 'GrammCategorySet', fields ['language', 'position']
        db.create_unique('wordengine_grammcategoryset', ['language_id', 'position'])

        # Adding M2M table for field gramm_category_multi on 'GrammCategorySet'
        m2m_table_name = db.shorten_name('wordengine_grammcategoryset_gramm_category_multi')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grammcategoryset', models.ForeignKey(orm['wordengine.grammcategoryset'], null=False)),
            ('grammcategory', models.ForeignKey(orm['wordengine.grammcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['grammcategoryset_id', 'grammcategory_id'])

        # Adding model 'Inflection'
        db.create_table('wordengine_inflection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Language'])),
            ('syntactic_category_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.SyntacticCategory'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('wordengine', ['Inflection'])

        # Adding model 'Lexeme'
        db.create_table('wordengine_lexeme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Language'])),
            ('syntactic_category', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.SyntacticCategory'], blank=True)),
            ('inflection', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.Inflection'], blank=True)),
        ))
        db.send_create_signal('wordengine', ['Lexeme'])

        # Adding model 'TranslatedTerm'
        db.create_table('wordengine_translatedterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Language'])),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_id', self.gf('django.db.models.fields.IntegerField')()),
            ('term_full_translation', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('term_abbr_translation', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('wordengine', ['TranslatedTerm'])

        # Adding model 'Translation'
        db.create_table('wordengine_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lexeme_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translationbase_fst_set', to=orm['wordengine.Lexeme'])),
            ('lexeme_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translationbase_snd_set', to=orm['wordengine.Lexeme'])),
        ))
        db.send_create_signal('wordengine', ['Translation'])

        # Adding M2M table for field source on 'Translation'
        m2m_table_name = db.shorten_name('wordengine_translation_source')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('translation', models.ForeignKey(orm['wordengine.translation'], null=False)),
            ('source', models.ForeignKey(orm['wordengine.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['translation_id', 'source_id'])

        # Adding M2M table for field usage_constraint_multi on 'Translation'
        m2m_table_name = db.shorten_name('wordengine_translation_usage_constraint_multi')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('translation', models.ForeignKey(orm['wordengine.translation'], null=False)),
            ('usageconstraint', models.ForeignKey(orm['wordengine.usageconstraint'], null=False))
        ))
        db.create_unique(m2m_table_name, ['translation_id', 'usageconstraint_id'])

        # Adding M2M table for field dialect_multi on 'Translation'
        m2m_table_name = db.shorten_name('wordengine_translation_dialect_multi')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('translation', models.ForeignKey(orm['wordengine.translation'], null=False)),
            ('dialect', models.ForeignKey(orm['wordengine.dialect'], null=False))
        ))
        db.create_unique(m2m_table_name, ['translation_id', 'dialect_id'])

        # Adding model 'Wordform'
        db.create_table('wordengine_wordform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Lexeme'])),
            ('gramm_category_set', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.GrammCategorySet'], blank=True)),
            ('spelling', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('writing_system', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.WritingSystem'], blank=True)),
        ))
        db.send_create_signal('wordengine', ['Wordform'])

        # Adding M2M table for field source on 'Wordform'
        m2m_table_name = db.shorten_name('wordengine_wordform_source')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordform', models.ForeignKey(orm['wordengine.wordform'], null=False)),
            ('source', models.ForeignKey(orm['wordengine.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordform_id', 'source_id'])

        # Adding M2M table for field dialect_multi on 'Wordform'
        m2m_table_name = db.shorten_name('wordengine_wordform_dialect_multi')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordform', models.ForeignKey(orm['wordengine.wordform'], null=False)),
            ('dialect', models.ForeignKey(orm['wordengine.dialect'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordform_id', 'dialect_id'])

        # Adding model 'WordformSample'
        db.create_table('wordengine_wordformsample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lexeme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordengine.Lexeme'])),
            ('gramm_category_set', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.GrammCategorySet'], blank=True)),
            ('spelling', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('writing_system', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['wordengine.WritingSystem'], blank=True)),
            ('informant', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('wordengine', ['WordformSample'])

        # Adding M2M table for field source on 'WordformSample'
        m2m_table_name = db.shorten_name('wordengine_wordformsample_source')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordformsample', models.ForeignKey(orm['wordengine.wordformsample'], null=False)),
            ('source', models.ForeignKey(orm['wordengine.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordformsample_id', 'source_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GrammCategorySet', fields ['language', 'position']
        db.delete_unique('wordengine_grammcategoryset', ['language_id', 'position'])

        # Deleting model 'SyntacticCategory'
        db.delete_table('wordengine_syntacticcategory')

        # Deleting model 'UsageConstraint'
        db.delete_table('wordengine_usageconstraint')

        # Deleting model 'GrammCategoryType'
        db.delete_table('wordengine_grammcategorytype')

        # Deleting model 'GrammCategory'
        db.delete_table('wordengine_grammcategory')

        # Deleting model 'Language'
        db.delete_table('wordengine_language')

        # Removing M2M table for field syntactic_category_multi on 'Language'
        db.delete_table(db.shorten_name('wordengine_language_syntactic_category_multi'))

        # Deleting model 'SourceType'
        db.delete_table('wordengine_sourcetype')

        # Deleting model 'Source'
        db.delete_table('wordengine_source')

        # Deleting model 'DictChange'
        db.delete_table('wordengine_dictchange')

        # Deleting model 'FieldChange'
        db.delete_table('wordengine_fieldchange')

        # Deleting model 'Dialect'
        db.delete_table('wordengine_dialect')

        # Deleting model 'WritingSystemType'
        db.delete_table('wordengine_writingsystemtype')

        # Deleting model 'WritingSystem'
        db.delete_table('wordengine_writingsystem')

        # Deleting model 'GrammCategorySet'
        db.delete_table('wordengine_grammcategoryset')

        # Removing M2M table for field gramm_category_multi on 'GrammCategorySet'
        db.delete_table(db.shorten_name('wordengine_grammcategoryset_gramm_category_multi'))

        # Deleting model 'Inflection'
        db.delete_table('wordengine_inflection')

        # Deleting model 'Lexeme'
        db.delete_table('wordengine_lexeme')

        # Deleting model 'TranslatedTerm'
        db.delete_table('wordengine_translatedterm')

        # Deleting model 'Translation'
        db.delete_table('wordengine_translation')

        # Removing M2M table for field source on 'Translation'
        db.delete_table(db.shorten_name('wordengine_translation_source'))

        # Removing M2M table for field usage_constraint_multi on 'Translation'
        db.delete_table(db.shorten_name('wordengine_translation_usage_constraint_multi'))

        # Removing M2M table for field dialect_multi on 'Translation'
        db.delete_table(db.shorten_name('wordengine_translation_dialect_multi'))

        # Deleting model 'Wordform'
        db.delete_table('wordengine_wordform')

        # Removing M2M table for field source on 'Wordform'
        db.delete_table(db.shorten_name('wordengine_wordform_source'))

        # Removing M2M table for field dialect_multi on 'Wordform'
        db.delete_table(db.shorten_name('wordengine_wordform_dialect_multi'))

        # Deleting model 'WordformSample'
        db.delete_table('wordengine_wordformsample')

        # Removing M2M table for field source on 'WordformSample'
        db.delete_table(db.shorten_name('wordengine_wordformsample_source'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wordengine.dialect': {
            'Meta': {'object_name': 'Dialect'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.Language']", 'blank': 'True'}),
            'parent_dialect': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.Dialect']", 'blank': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.dictchange': {
            'Meta': {'object_name': 'DictChange'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'object_type': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'timestamp_change': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timestamp_review': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_changer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wordengine_dictchange_changer'", 'to': "orm['auth.User']"}),
            'user_reviewer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']", 'blank': 'True'})
        },
        'wordengine.fieldchange': {
            'Meta': {'object_name': 'FieldChange'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'object_type': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'timestamp_change': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_changer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wordengine_fieldchange_changer'", 'to': "orm['auth.User']"})
        },
        'wordengine.grammcategory': {
            'Meta': {'object_name': 'GrammCategory'},
            'gramm_category_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.GrammCategoryType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.grammcategoryset': {
            'Meta': {'unique_together': "(('language', 'position'),)", 'object_name': 'GrammCategorySet'},
            'gramm_category_multi': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['wordengine.GrammCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Language']"}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'syntactic_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.SyntacticCategory']"})
        },
        'wordengine.grammcategorytype': {
            'Meta': {'object_name': 'GrammCategoryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.inflection': {
            'Meta': {'object_name': 'Inflection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Language']"}),
            'syntactic_category_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.SyntacticCategory']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'wordengine.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'syntactic_category_multi': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['wordengine.SyntacticCategory']"}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.lexeme': {
            'Meta': {'object_name': 'Lexeme'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflection': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.Inflection']", 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Language']"}),
            'syntactic_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.SyntacticCategory']", 'blank': 'True'})
        },
        'wordengine.source': {
            'Meta': {'object_name': 'Source'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.Language']", 'blank': 'True'}),
            'source_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.SourceType']"}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.sourcetype': {
            'Meta': {'object_name': 'SourceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.syntacticcategory': {
            'Meta': {'object_name': 'SyntacticCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.translatedterm': {
            'Meta': {'object_name': 'TranslatedTerm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Language']"}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'term_abbr_translation': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full_translation': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'term_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'wordengine.translation': {
            'Meta': {'object_name': 'Translation'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dialect_multi': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.Dialect']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lexeme_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translationbase_fst_set'", 'to': "orm['wordengine.Lexeme']"}),
            'lexeme_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translationbase_snd_set'", 'to': "orm['wordengine.Lexeme']"}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.Source']", 'blank': 'True'}),
            'usage_constraint_multi': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.UsageConstraint']", 'blank': 'True'})
        },
        'wordengine.usageconstraint': {
            'Meta': {'object_name': 'UsageConstraint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'wordengine.wordform': {
            'Meta': {'object_name': 'Wordform'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dialect_multi': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.Dialect']", 'blank': 'True'}),
            'gramm_category_set': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.GrammCategorySet']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Lexeme']"}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.Source']", 'blank': 'True'}),
            'spelling': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'writing_system': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.WritingSystem']", 'blank': 'True'})
        },
        'wordengine.wordformsample': {
            'Meta': {'object_name': 'WordformSample'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gramm_category_set': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.GrammCategorySet']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informant': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lexeme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.Lexeme']"}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['wordengine.Source']", 'blank': 'True'}),
            'spelling': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'writing_system': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.WritingSystem']", 'blank': 'True'})
        },
        'wordengine.writingsystem': {
            'Meta': {'object_name': 'WritingSystem'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['wordengine.Language']", 'blank': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'writing_system_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordengine.WritingSystemType']"})
        },
        'wordengine.writingsystemtype': {
            'Meta': {'object_name': 'WritingSystemType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term_abbr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'term_full': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['wordengine']