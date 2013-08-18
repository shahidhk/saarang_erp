# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.time_destin_core_approval'
        db.alter_column('task_task', 'time_destin_core_approval', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Task.author'
        db.alter_column('task_task', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Task.destin_dept'
        db.alter_column('task_task', 'destin_dept_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['erp.Department']))

        # Changing field 'Task.time_origin_core_approval'
        db.alter_column('task_task', 'time_origin_core_approval', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Task.origin_dept'
        db.alter_column('task_task', 'origin_dept_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['erp.Department']))

        # Changing field 'Task.time_destn_coord_acknowledged'
        db.alter_column('task_task', 'time_destn_coord_acknowledged', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Comment.description'
        db.alter_column('task_comment', 'description', self.gf('django.db.models.fields.TextField')(max_length=1000))

    def backwards(self, orm):

        # Changing field 'Task.time_destin_core_approval'
        db.alter_column('task_task', 'time_destin_core_approval', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Task.author'
        db.alter_column('task_task', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(default='ee13b001', to=orm['auth.User']))

        # Changing field 'Task.destin_dept'
        db.alter_column('task_task', 'destin_dept_id', self.gf('django.db.models.fields.related.ForeignKey')(default='Design', to=orm['erp.Department']))

        # Changing field 'Task.time_origin_core_approval'
        db.alter_column('task_task', 'time_origin_core_approval', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Task.origin_dept'
        db.alter_column('task_task', 'origin_dept_id', self.gf('django.db.models.fields.related.ForeignKey')(default='Design', to=orm['erp.Department']))

        # Changing field 'Task.time_destn_coord_acknowledged'
        db.alter_column('task_task', 'time_destn_coord_acknowledged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Comment.description'
        db.alter_column('task_comment', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'erp.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'task.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_commented'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_task'", 'to': "orm['task.Task']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'destin_coord_acknowledged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destin_core_aproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destin_core_assgnd_coord': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'related_name': "'destin_core_assigned_coord_fortask'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'destin_core_comment': ('django.db.models.fields.CharField', [], {'default': "'No comment'", 'max_length': '200'}),
            'destin_core_deadline': ('django.db.models.fields.DateField', [], {'default': "'2013-08-18'"}),
            'destin_core_priority': ('django.db.models.fields.FloatField', [], {'default': '4.5'}),
            'destin_dept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_destination_dept'", 'null': 'True', 'to': "orm['erp.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin_core_aproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin_core_assgnd_coord': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'related_name': "'origin_core_assigned_coord_fortask'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'origin_core_comment': ('django.db.models.fields.CharField', [], {'default': "'No comment'", 'max_length': '200'}),
            'origin_core_deadline': ('django.db.models.fields.DateField', [], {'default': "'2013-08-18'"}),
            'origin_core_priority': ('django.db.models.fields.FloatField', [], {'default': '4.5'}),
            'origin_deadline': ('django.db.models.fields.DateField', [], {}),
            'origin_dept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_originating_dept'", 'null': 'True', 'to': "orm['erp.Department']"}),
            'origin_priority': ('django.db.models.fields.FloatField', [], {}),
            'percent_completed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_destin_core_approval': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 18, 0, 0)'}),
            'time_destn_coord_acknowledged': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 18, 0, 0)'}),
            'time_origin_core_approval': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 18, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['task']