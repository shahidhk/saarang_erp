from django.db import models
from registration.models import SaarangUser

class Team(models.Model):
    name = models.CharField(max_length=100)
    team_sid = models.CharField(max_length=20)
    leader = models.ForeignKey(SaarangUser,related_name='team_leader')
    members = models.ManyToManyField(SaarangUser,related_name='team_members', blank=True)
    ACCOMODATION_CHOICES = (
        ('not_req', 'Accomodation not required'),
        ('requested', 'Accomodation requested'),
        ('confirmed', 'Request confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('rejected', 'Rejected'),
        )
    accomodation_status = models.CharField(max_length=50, choices=ACCOMODATION_CHOICES, default='not_req')
    date_of_arrival = models.DateField(blank=True, null=True)
    time_of_arrival = models.TimeField(blank=True,null=True)
    date_of_departure =  models.DateField(blank=True, null=True)
    time_of_departure = models.TimeField(blank=True, null=True)
    def __unicode__(self):
        return (str(self.name) + ' lead by ' + str(self.leader))

    def get_total_count(self):
        mem = len(self.members.all())
        return mem+1