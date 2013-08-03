from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from erp.models import Department, Event
# Create your models here.
class Task(models.Model):
    time_created = models.DateTimeField(auto_now_add = True)
    origin_dept = models.ForeignKey(Department, related_name = 'task_originating_dept')
    destin_dept = models.ForeignKey(Department, related_name = 'task_destination_dept')
    title = models.CharField(max_length = 60, verbose_name = 'Title <60 letters>')
    summary = models.CharField(max_length = 200, verbose_name = 'Short summary of task <200 letters>')
    description= models.CharField(max_length = 1000, verbose_name = 'Long description of task <1000 letters>')
    attachment = models.FileField(upload_to = 'attachments')
    origin_deadline = models.DateField()
    origin_priority = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)')
    origin_core_aproved = models.BooleanField()
    time_origin_core_approval = models.DateTimeField(auto_now = True)
    origin_core_comment = models.CharField(max_length=200)
    origin_core_deadline = models.DateField()
    origin_core_priority = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)')
    origin_core_assgnd_coord = models.ManyToManyField(User, related_name = 'origin_core_assigned_coord_fortask')
    destin_core_aproved = models.BooleanField()
    time_destin_core_approval = models.DateTimeField(auto_now = True)
    destin_core_comment = models.CharField(max_length=200)
    destin_core_deadline = models.DateField()
    destin_core_priority = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Priority of the task in a scale 0 to 5 (eg. 4.5)')
    destin_core_assgnd_coord = models.ManyToManyField(User, related_name = 'destin_core_assigned_coord_fortask')
    destin_coord_acknowledged = models.BooleanField()
    time_destn_coord_acknowledged = models.DateTimeField(auto_now=True)
    percent_completed = models.IntegerField(max_length=3)
    is_completed = models.BooleanField()
    
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='user_commented')
    timestamp = models.DateTimeField(auto_now_add = True)
    task = models.ForeignKey('Task', related_name = 'parent_task')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)