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
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class ItemRequest(models.Model):
    item_request = models.CharField(max_length=2000)
    total_cost = models.IntegerField()
    request_by = models.ForeignKey(UserProfile,related_name='request_by')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Request by %s' %(self.request_by) 

    def get_item_list(self):
        item_list=[]
        for item in self.item_request.split(';'):
            item_list.append([item.split('=')[0],item.split('=')[1]])
        return item_list

    def update(self):
        for item in self.item_request.split(';'):
            item = item.split('=')
            item_n = Item.objects.get(name=item[0])
            item_n.count+=int(item[1])
            item_n.save()

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
    refreshment_cost = models.IntegerField(default=0)
    number_of_people = models.IntegerField(default=0)
    comments = models.TextField(max_length=2500,blank=True)

    def __unicode__(self):
        return '%d people staying' %(self.number_of_people)

class TransportRequest(models.Model):
    number_of_people = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)     
    comments = models.TextField(max_length=2500,blank=True)

    def __unicode__(self):
        return '%d people for transport' %(self.number_of_people)

class EventRequest(models.Model):
    event = models.ForeignKey(Event,related_name='event_request',blank=True,null=True)
    fr_request = models.ForeignKey(ItemRequest,related_name='fr_request',blank=True,null=True)
    hospi_request = models.ForeignKey(HospitalityRequest,related_name='hospi_request',blank=True,null=True)
    trans_request = models.ForeignKey(TransportRequest,related_name='trans_request',blank=True,null=True)
    memento_request = models.ForeignKey(MementoRequest,related_name='mem_request',blank=True,null=True)
    misc = models.TextField(max_length=2500,blank=True)
    submitted = models.BooleanField(default=False)
    