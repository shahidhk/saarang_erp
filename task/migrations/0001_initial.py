# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table('task_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_created', null=True, to=orm['auth.User'])),
            ('origin_dept', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task_originating_dept', null=True, to=orm['erp.Department'])),
            ('destin_dept', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task_destination_dept', null=True, to=orm['erp.Department'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('origin_deadline', self.gf('django.db.models.fields.DateField')()),
            ('origin_priority', self.gf('django.db.models.fields.FloatField')()),
            ('origin_core_aproved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_origin_core_approval', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 25, 0, 0))),
            ('origin_core_comment', self.gf('django.db.models.fields.CharField')(default='No comment', max_length=200)),
            ('origin_core_deadline', self.gf('django.db.models.fields.DateField')(default='2013-10-25')),
            ('origin_core_priority', self.gf('django.db.models.fields.FloatField')(default=4.5)),
            ('destin_core_aproved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_destin_core_approval', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 25, 0, 0))),
            ('destin_core_comment', self.gf('django.db.models.fields.CharField')(default='No comment', max_length=200)),
            ('destin_core_deadline', self.gf('django.db.models.fields.DateField')(default='2013-10-25')),
            ('destin_core_priority', self.gf('django.db.models.fields.FloatField')(default=4.5)),
            ('destin_coord_acknowledged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_destn_coord_acknowledged', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 25, 0, 0))),
            ('percent_completed', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('task', ['Task'])

        # Adding M2M table for field origin_core_assgnd_coord on 'Task'
        m2m_table_name = db.shorten_name('task_task_origin_core_assgnd_coord')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['task.task'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'user_id'])

        # Adding M2M table for field destin_core_assgnd_coord on 'Task'
        m2m_table_name = db.shorten_name('task_task_destin_core_assgnd_coord')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['task.task'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'user_id'])

        # Adding model 'Comment'
        db.create_table('task_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_commented', to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_task', to=orm['task.Task'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal('task', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table('task_task')

        # Removing M2M table for field origin_core_assgnd_coord on 'Task'
        db.delete_table(db.shorten_name('task_task_origin_core_assgnd_coord'))

        # Removing M2M table for field destin_core_assgnd_coord on 'Task'
        db.delete_table(db.shorten_name('task_task_destin_core_assgnd_coord'))

        # Deleting model 'Comment'
        db.delete_table('task_comment')


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
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'destin_coord_acknowledged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destin_core_aproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'destin_core_assgnd_coord': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'related_name': "'destin_core_assigned_coord_fortask'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'destin_core_comment': ('django.db.models.fields.CharField', [], {'default': "'No comment'", 'max_length': '200'}),
            'destin_core_deadline': ('django.db.models.fields.DateField', [], {'default': "'2013-10-25'"}),
            'destin_core_priority': ('django.db.models.fields.FloatField', [], {'default': '4.5'}),
            'destin_dept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_destination_dept'", 'null': 'True', 'to': "orm['erp.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin_core_aproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin_core_assgnd_coord': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'related_name': "'origin_core_assigned_coord_fortask'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'origin_core_comment': ('django.db.models.fields.CharField', [], {'default': "'No comment'", 'max_length': '200'}),
            'origin_core_deadline': ('django.db.models.fields.DateField', [], {'default': "'2013-10-25'"}),
            'origin_core_priority': ('django.db.models.fields.FloatField', [], {'default': '4.5'}),
            'origin_deadline': ('django.db.models.fields.DateField', [], {}),
            'origin_dept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_originating_dept'", 'null': 'True', 'to': "orm['erp.Department']"}),
            'origin_priority': ('django.db.models.fields.FloatField', [], {}),
            'percent_completed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_destin_core_approval': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 25, 0, 0)'}),
            'time_destn_coord_acknowledged': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 25, 0, 0)'}),
            'time_origin_core_approval': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 25, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['task']