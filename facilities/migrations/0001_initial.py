# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'user'
        db.create_table('facilities_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('facilities', ['user'])

        # Adding model 'facilities'
        db.create_table('facilities_facilities', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone', self.gf('django.db.models.fields.FloatField')()),
            ('ip_date', self.gf('django.db.models.fields.DateField')(default='28 -10 -2013')),
            ('ip_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('ip_copies', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('ven_date', self.gf('django.db.models.fields.DateField')(default='28 -10 -2013')),
            ('ven_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('ven_wifi', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ven_ac', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ven_foot', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('ven_sugg', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('ven_comments', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('equip_date', self.gf('django.db.models.fields.DateField')(default='28 -10 -2013')),
            ('equip_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('equip_ven', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('equip_mreq', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('equip_comm', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('trans_bdate', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('trans_jname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('trans_noppl', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('trans_bpicloc', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('trans_btime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('trans_bdes', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('trans_atime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('trans_adroloc', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('trans_ades', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('facilities', ['facilities'])


    def backwards(self, orm):
        # Deleting model 'user'
        db.delete_table('facilities_user')

        # Deleting model 'facilities'
        db.delete_table('facilities_facilities')


    models = {
        'facilities.facilities': {
            'Meta': {'object_name': 'facilities'},
            'equip_comm': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'equip_date': ('django.db.models.fields.DateField', [], {'default': "'28 -10 -2013'"}),
            'equip_mreq': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'equip_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'equip_ven': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_copies': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'ip_date': ('django.db.models.fields.DateField', [], {'default': "'28 -10 -2013'"}),
            'ip_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'phone': ('django.db.models.fields.FloatField', [], {}),
            'trans_ades': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'trans_adroloc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_atime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_bdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_bdes': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_bpicloc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_btime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_jname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_noppl': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ven_ac': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ven_comments': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'ven_date': ('django.db.models.fields.DateField', [], {'default': "'28 -10 -2013'"}),
            'ven_foot': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'ven_sugg': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'ven_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'ven_wifi': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'facilities.user': {
            'Meta': {'object_name': 'user'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['facilities']