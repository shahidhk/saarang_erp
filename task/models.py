from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from erp.models import Department, Event
import datetime
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
# Create your models here.
class Task(models.Model):
    time_created = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, related_name='user_created')
    origin_dept = models.ForeignKey(Department, related_name = 'task_originating_dept')
    destin_dept = models.ForeignKey(Department, related_name = 'task_destination_dept')
    title = models.CharField(max_length = 60, verbose_name = 'Title <60 letters>')
    summary = models.CharField(max_length = 200, verbose_name = 'Short summary of task <200 letters>')
    description= models.TextField(max_length = 1000, verbose_name = 'Long description of task <1000 letters>')
    attachment = models.FileField(upload_to = 'attachments', blank=True, null=True)
    origin_deadline = models.DateField()
    origin_priority = models.FloatField(verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)')
    origin_core_aproved = models.BooleanField(default=False)
    time_origin_core_approval = models.DateTimeField(auto_now = True, default = now)
    origin_core_comment = models.CharField(max_length=200, default="No comment")
    origin_core_deadline = models.DateField(default=date)
    origin_core_priority = models.FloatField(verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)', default=4.5)
    origin_core_assgnd_coord = models.ManyToManyField(User, related_name = 'origin_core_assigned_coord_fortask', default =1)
    destin_core_aproved = models.BooleanField(default=False)
    time_destin_core_approval = models.DateTimeField(auto_now = True, default=now)
    destin_core_comment = models.CharField(max_length=200, default= "No comment")
    destin_core_deadline = models.DateField(default=date)
    destin_core_priority = models.FloatField(verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)', default=4.5)
    destin_core_assgnd_coord = models.ManyToManyField(User, related_name = 'destin_core_assigned_coord_fortask', default=1)
    destin_coord_acknowledged = models.BooleanField(default=False)
    time_destn_coord_acknowledged = models.DateTimeField(auto_now=True, default=now)
    percent_completed = models.IntegerField(max_length=3, default=0)
    is_completed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='user_commented')
    timestamp = models.DateTimeField(auto_now_add = True)
    task = models.ForeignKey('Task', related_name = 'parent_task')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.title