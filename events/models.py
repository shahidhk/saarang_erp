from django.db import models
from django.contrib.auth.models import User

from erp.models import SubDepartment
from registration.models import SaarangUser

class Event(models.Model):
    name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=100)
    oneliner = models.CharField(max_length=250,blank=True)
    sub_dept = models.ForeignKey(SubDepartment, related_name='parent_department')
    google_group = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    CATEGORY_CHOICES = (
        ('Onsite', 'Onsite'),
        ('Online', 'Online'),
        ('Pre-registered', 'Pre registerd'),
        )
    registration_info = models.TextField(max_length=2000,blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50,blank=True)
    event_format = models.TextField(max_length=3000,blank=True,null=True)
    about = models.TextField(max_length=3000,blank=True,null=True)
    faqs = models.ManyToManyField('FAQ',related_name='event_faq',blank=True,null=True)
    FAQs = models.TextField(max_length=5000,blank=True,null=True)
    prizes = models.TextField(max_length=3000,blank=True,null=True)
    is_team = models.BooleanField(default=False,verbose_name='Team Event')
    registration_open = models.BooleanField(default=True)
    registration_close_date = models.DateField(blank=True,null=True)
    contacts = models.TextField(max_length=700,blank=True,null=True)
    options = models.CharField(max_length=5000,blank=True)
    
    def __unicode__(self):
        return self.long_name


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=1000)

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(SaarangUser,related_name='team_leader')
    members = models.ManyToManyField(SaarangUser,related_name='team_member')
    def __unicode__(self):
        return (str(self.name) + ' lead by ' + str(self.leader))

class EventRegistration(models.Model):
    participant = models.ForeignKey(SaarangUser,related_name='event_reg_user')
    event = models.ForeignKey(Event,related_name='reg_event')
    team = models.ForeignKey(Team,related_name='event_reg_team',blank=True,null=True)
    is_participating = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(blank=True,null=True,auto_now_add=True)

    def __unicode__(self):
        return str(self.participant) +' for ' + str(self.event)

