# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'facilities.equip_time'
        db.alter_column('facilities_facilities', 'equip_time', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'facilities.ven_time'
        db.alter_column('facilities_facilities', 'ven_time', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'facilities.ip_time'
        db.alter_column('facilities_facilities', 'ip_time', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'facilities.trans_atime'
        db.alter_column('facilities_facilities', 'trans_atime', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'facilities.trans_btime'
        db.alter_column('facilities_facilities', 'trans_btime', self.gf('django.db.models.fields.TimeField')())

    def backwards(self, orm):

        # Changing field 'facilities.equip_time'
        db.alter_column('facilities_facilities', 'equip_time', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'facilities.ven_time'
        db.alter_column('facilities_facilities', 'ven_time', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'facilities.ip_time'
        db.alter_column('facilities_facilities', 'ip_time', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'facilities.trans_atime'
        db.alter_column('facilities_facilities', 'trans_atime', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'facilities.trans_btime'
        db.alter_column('facilities_facilities', 'trans_btime', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'facilities.facilities': {
            'Meta': {'object_name': 'facilities'},
            'equip_comm': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'equip_date': ('django.db.models.fields.DateField', [], {'default': "'2013-10-28'"}),
            'equip_mreq': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'equip_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'equip_ven': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_copies': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'ip_date': ('django.db.models.fields.DateField', [], {'default': "'2013-10-28'"}),
            'ip_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'phone': ('django.db.models.fields.FloatField', [], {}),
            'trans_ades': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'trans_adroloc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_atime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_bdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_bdes': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_bpicloc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_btime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'trans_jname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trans_noppl': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ven_ac': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ven_comments': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'ven_date': ('django.db.models.fields.DateField', [], {'default': "'2013-10-28'"}),
            'ven_foot': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'ven_sugg': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'ven_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
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