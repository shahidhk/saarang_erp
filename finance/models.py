from django.db import models

from userprofile.models import UserProfile
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

    def save(self,*args, **kwargs):
        for item in self.item_request.split(';'):
            item = item.split('=')
            item_n = Item.objects.get(name=item[0])
            item_n.count+=int(item[1])
            item_n.save()

        super(Model, self).save(*args, **kwargs)

class Memento(models.Model):
    name = models.CharField(max_length=100,verbose_name='Name of the Memento',unique=True)
    cost = models.IntegerField()
    description = models.TextField(max_length=1000,blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name