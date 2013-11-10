from django.db import models
from userprofile.models import User
from erp.models import Department,SubDepartment
from events.models import Event
# Create your models here.

class Notification(models.Model):
    notif_body = models.CharField(max_length=300,verbose_name='Notification Content')
    timestamp = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=50)
    receive_users = models.ManyToManyField(User,related_name='re_users',blank=True,null=True)
    receive_depts = models.ManyToManyField(Department,related_name='re_depts',blank=True,null=True)
    receive_subdepts = models.ManyToManyField(SubDepartment,related_name='re_subdepts',blank=True,null=True)
    receive_events = models.ManyToManyField(Event,related_name='re_events',blank=True,null=True)
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.notif_body

