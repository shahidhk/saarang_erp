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
    is_active = models.BooleanField(default=True)   
    visible_fields = models.CharField(max_length=10,blank=True,default='11111',verbose_name='Is Active')

    def __unicode__(self):
        return self.long_name

    def get_participants_count(self):
        return len(self.reg_event.all())

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=1000)

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(SaarangUser,related_name='team_leader')
    members = models.ManyToManyField(SaarangUser,related_name='team_members', blank=True)
    team_sid = models.CharField(max_length=20)
    ACCOMODATION_CHOICES = (
        ('not_req', 'Accomodation not required'),
        ('requested', 'Accomodation requested'),
        ('confirmed', 'Request confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('rejected', 'Rejected'),
    )
    accomodation_status = models.CharField(max_length=50, choices=ACCOMODATION_CHOICES, default='not_req')
    date_of_arrival = models.DateField(blank=True, null=True, default='2014-01-08')
    time_of_arrival = models.TimeField(blank=True,null=True, default='23:00:00')
    date_of_departure =  models.DateField(blank=True, null=True, default='2014-01-11')
    time_of_departure = models.TimeField(blank=True, null=True, default='10:00:00')
    CHECKED_CHOICES = (
        ('in', 'in'),
        ('out', 'out'),
        )
    checked_status = models.CharField(max_length=50, choices=CHECKED_CHOICES, default='out')
    def __unicode__(self):
        try:
            ret_val = (str(self.name)+ ' lead by '+ str(self.leader))
        except Exception,e:
            ret_val = 'None'
        return ret_val

    def get_total_count(self):
        mem = len(self.members.all())
        return mem+1

    def get_male_count(self):
        mem = len(self.members.all().filter(gender='male'))
        if self.leader.gender == 'male':
            mem +=1
        return mem

    def get_female_count(self):
        mem = len(self.members.all().filter(gender='female'))
        if self.leader.gender == 'female':
            mem +=1
        return mem

    # def is_mixed(self):
    #     if self.get_female_count() and self.get_male_count():
    #         return True
    #     else:
    #         return False

    def get_male_members(self):
        mem = list(self.members.filter(gender='male'))
        if self.leader.gender == 'male':
            mem.append(self.leader)
        return mem

    def get_female_members(self):
        mem = list(self.members.filter(gender='female'))
        if self.leader.gender == 'female':
            mem.append(self.leader)
        return mem

class EventRegistration(models.Model):
    participant = models.ForeignKey(SaarangUser,related_name='event_reg_user')
    event = models.ForeignKey(Event,related_name='reg_event')
    team = models.ForeignKey(Team,related_name='event_reg_team',blank=True,null=True)
    is_participating = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    options = models.TextField(max_length=10000,blank=True,null=True,default='')
    # url1 = models.URLField(max_length=500)
    # url2 = models.URLField(max_length=500)

    def __unicode__(self):
        return str(self.participant) +' for ' + str(self.event)

# class Slot(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, related_name='slot_created_user')
#     VENUE_CHOICES = (
#         ('CLT', 'CLT' ),
#         ('ICSR Main Auditorium', 'ICSR Main Auditorium'),
#         ('ICSR Hall 1', 'ICSR Hall 1'),
#         ('ICSR Hall 2', 'ICSR Hall 2'),
#         ('ICSR Hall 3', 'ICSR Hall 3'),
#         ('ICSR Dining Hall', 'ICSR Dining Hall'),
#         ('DoMS 101', 'DoMS 101'),
#         ('DoMS 401', 'DoMS 401'),
#         ('DoMS 402', 'DoMS 402'),
#         ('CRC 101', 'CRC 101'),
#         ('CRC 102', 'CRC 102'),
#         ('CRC 103', 'CRC 103'),
#         ('CRC 201', 'CRC 201'),
#         ('CRC 202', 'CRC 202'),
#         ('CRC 203', 'CRC 203'),
#         ('Bindaas Park', 'Bindaas Park'),
#         ('FA Hut', 'FA Hut'),
#         ('Informals Hut', 'Informals Hut'),
#         ('OAT', 'OAT'),
#         ('SAC', 'SAC'),
#         ('BSB', 'BSB'),
#         ('Adventure Zone', 'Adventure Zone'),
#         ('KV Grounds', 'KV Grounds'),
#         ('Mahanadhi Playground', 'Mahanadhi Playground'),
#         ('Carnival Stage', 'Carnival Stage'),
#         ('HSB 357', 'HSB 357'),
#         ('PhLT', 'PhLT'),        
#     )
#     DAY_CHOICES = (
#         ('0', 'Day 0 (8th Jan 2014 Wed)'),
#         ('1', 'Day 1 (9th Jan 2014 Thu)'),
#         ('2', 'Day 2 (10th Jan 2014 Thu)'),
#         ('3', 'Day 3 (11th Jan 2014 Fri)'),
#         ('4', 'Day 4 (12th Jan 2014 Sat)'),
#     )
#     venue = models.CharField(choices=VENUE_CHOICES, max_length=50)
#     day = models.CharField(choices=DAY_CHOICES, max_length=50)
#     start_time = models.TimeField(default='09:00:00')
#     end_time = models.TimeField(default='10:00:00')
#     comments = models.TextField(blank=True, null=True)
