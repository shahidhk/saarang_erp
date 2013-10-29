# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sub_dept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_department', to=orm['erp.SubDepartment'])),
            ('google_group', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('registration_info', self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('event_format', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
            ('FAQs', self.gf('django.db.models.fields.TextField')(max_length=5000, null=True, blank=True)),
            ('prizes', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding M2M table for field faqs on 'Event'
        m2m_table_name = db.shorten_name('events_event_faqs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('faq', models.ForeignKey(orm['events.faq'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'faq_id'])

        # Adding model 'FAQ'
        db.create_table('events_faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal('events', ['FAQ'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('events_event')

        # Removing M2M table for field faqs on 'Event'
        db.delete_table(db.shorten_name('events_event_faqs'))

        # Deleting model 'FAQ'
        db.delete_table('events_faq')


    models = {
        'erp.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'erp.subdepartment': {
            'Meta': {'object_name': 'SubDepartment'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_dept'", 'to': "orm['erp.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'events.event': {
            'FAQs': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Event'},
            'about': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'event_format': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'faqs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_faq'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['events.FAQ']"}),
            'google_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'prizes': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'registration_info': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'sub_dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_department'", 'to': "orm['erp.SubDepartment']"})
        },
        'events.faq': {
            'Meta': {'object_name': 'FAQ'},
            'answer': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['events']