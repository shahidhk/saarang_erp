from django.db import models

from userprofile.models import UserProfile
from events.models import Event
# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name='Item name',unique=True)
    cost = models.IntegerField(verbose_name='Cost of a single unit')
    description = models.TextField(max_length=1000,blank=True,verbose_name='Description/comments')
    is_active = models.BooleanField(default=True,verbose_name='Valid?')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class ItemRequest(models.Model):
    item = models.ForeignKey(Item,related_name='related_item',blank=True,null=True)
    count = models.IntegerField(default=0)
    count_approved = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %d,' %(self.item,self.count) 

class Memento(models.Model):
    name = models.CharField(max_length=100,verbose_name='Name of the Memento',unique=True)
    cost = models.IntegerField()
    description = models.TextField(max_length=1000,blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    submitted = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class MementoRequest(models.Model):
    memento_request = models.CharField(max_length=2000)
    total_cost = models.IntegerField(default=0)
    request_by = models.ForeignKey(UserProfile,related_name='mem_request_by')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Memento request by %s' %(self.request_by) 

    def get_memento_list(self):
        memento_list=[]
        for memento in self.memento_request.split(';'):
            memento_list.append([memento.split('=')[0],memento.split('=')[1]])
        return memento_list

    def update(self):
        for memento in self.memento_request.split(';'):
            memento = memento.split('=')
            memento_n = Memento.objects.get(name=memento[0])
            memento_n.count+=int(memento[1])
            memento_n.save()

class HospitalityRequest(models.Model):
    accomodation_cost = models.IntegerField(default=0)
    approved_acc = models.BooleanField(default=False)
    refreshment_cost = models.IntegerField(default=0)
    approved_ref = models.BooleanField(default=False)
    number_of_people = models.IntegerField(default=0)
    comments = models.TextField(max_length=2500,blank=True)

    def __unicode__(self):
        return '%d people staying' %(self.number_of_people)

class TransportRequest(models.Model):
    number_of_people = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)     
    comments = models.TextField(max_length=2500,blank=True)

    def __unicode__(self):
        return '%d people for transport' %(self.number_of_people)

class Comments(models.Model):
    comment = models.TextField(max_length=10000,blank=True,null=True)
    by = models.ForeignKey(UserProfile,related_name='comment_by',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class MiscRequest(models.Model):
    amount = models.IntegerField(default=0)
    reason = models.CharField(max_length=1500,blank=True)
    request_by = models.ForeignKey(UserProfile,related_name='misc_request_by',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comments,related_name='misc_comments',blank=True,null=True)
    approved = models.BooleanField(default=False)

class EventRequest(models.Model):
    event = models.ForeignKey(Event,related_name='event_request',blank=True,null=True)
    item_request = models.ManyToManyField(ItemRequest,related_name='related_item_request',blank=True,null=True)
    hospi_request = models.ForeignKey(HospitalityRequest,related_name='hospi_request',blank=True,null=True)
    trans_request = models.ForeignKey(TransportRequest,related_name='trans_request',blank=True,null=True)
    memento_request = models.ForeignKey(MementoRequest,related_name='mem_request',blank=True,null=True)
    memento_number = models.IntegerField(default=0)
    number_of_prizes = models.IntegerField(default=0)
    ppm_comments = models.TextField(max_length=2500,blank=True)
    prizes = models.CharField(max_length=500,blank=True)
    submitted = models.BooleanField(default=False)
    request_by = models.ForeignKey(UserProfile,related_name='request_by',blank=True,null=True)
    prizes_approved = models.CharField(max_length=50,blank=True)
    memento_aaproved = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    misc_list = models.ManyToManyField(MiscRequest,related_name='misc_request',blank=True,null=True)
    comments = models.ManyToManyField(Comments,related_name='event_request_comments',blank=True,null=True)
    total_cost = models.IntegerField(default=0)