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
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='parent_department', null=True, to=orm['erp.Department'])),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('google_group', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ideation', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('spons_writeup', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('publicity_writeup', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('hospi_writeup', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('format_rules', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('inter_dept_rels', self.gf('django.db.models.fields.TextField')(max_length=1500)),
            ('prev_data', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('events_event')


    models = {
        'erp.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_department'", 'null': 'True', 'to': "orm['erp.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'format_rules': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'google_group': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hospi_writeup': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ideation': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'inter_dept_rels': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'prev_data': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'publicity_writeup': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'spons_writeup': ('django.db.models.fields.TextField', [], {'max_length': '1500'})
        }
    }

    complete_apps = ['events']