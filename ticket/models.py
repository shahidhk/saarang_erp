from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile
# Create your models here.
class Ticket(models.Model):
    ticket_name = models.CharField(max_length=100)
    SHOW = (('Rock Show','Rock Show'),('Choreo Night','Choreo Night'),('Popular Night','Popular Night'),('EDM','EDM'))
    ticket_show = models.CharField(max_length=20,choices=SHOW)
    ticket_is_discounted = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.ticket_name

class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket,related_name='trans_ticket')
    ticket_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ticket.ticket_name

class Transaction_final(models.Model):
    ticket_final = models.ManyToManyField(Transaction,related_name='trans_final',blank=True,null=True)
    customer_id = models.CharField(max_length=100,blank=True)
    coord = models.ForeignKey(UserProfile,related_name='sold_by')
    timestamp = models.DateTimeField(auto_now_add=True)
    challan_number = models.CharField(max_length=25)
    cost = models.IntegerField(default=0)

    def __unicode__(self):
        ret=''
        for item in self.ticket_final.all():
            ret+=item.ticket.ticket_name
        return ret
