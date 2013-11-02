# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SaarangUser'
        db.create_table('registration_saaranguser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('saarang_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('mobile', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('friend_list', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('fb_token', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('registration', ['SaarangUser'])


    def backwards(self, orm):
        # Deleting model 'SaarangUser'
        db.delete_table('registration_saaranguser')


    models = {
        'registration.saaranguser': {
            'Meta': {'object_name': 'SaarangUser'},
            'college': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fb_token': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'friend_list': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'saarang_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['registration']