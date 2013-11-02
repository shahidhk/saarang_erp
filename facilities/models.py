from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User, Group
#from erp.models import Department
from events.models import Event
import datetime
now=datetime.datetime.now()
date=now.strftime("%Y-%m-%d")
materials=(
		('sci', 'Scissors'),
		('ch' , 'Chairs'),
		('tab' , 'Tables'),
		)
	
class Fac_Ip(models.Model):
    user=models.ForeignKey(User, related_name='user_ip', blank=True)
    phone=models.FloatField()
    ip_date=models.DateField(default = date , verbose_name='date')
    ip_time=models.TimeField(default = now , verbose_name='time')
    ip_copies=models.IntegerField(max_length=5 , verbose_name='no. of copies')

class Materials(models.Model):
    mat_item=models.CharField(max_length=15, choices=materials)
    mat_num=models.IntegerField()


class Fac_Ven(models.Model):
    user=models.ForeignKey(User, related_name='user_ven', blank=True)
    phone=models.FloatField()
    ven_date=models.DateField(default=date , verbose_name='date')
    ven_time=models.TimeField(default=now , verbose_name='time')
    ven_wifi=models.BooleanField(default=False , verbose_name='Wi-Fi')
    ven_ac=models.BooleanField(default=False , verbose_name='A/C')
    ven_foot=models.IntegerField(max_length=5, verbose_name='Estimated Footfall')
    ven_sugg=models.CharField(max_length=15, verbose_name='Suggested venues', blank=True)
    ven_comments=models.TextField(max_length=2000, verbose_name='Comments', blank=True)
    
class Fac_Equip(models.Model):
    user=models.ForeignKey(User, related_name='user_equip' )
    phone=models.FloatField()
    equip_date=models.DateField(default=date , verbose_name='date')
    equip_time=models.TimeField(default=now , verbose_name='time')
    equip_ven=models.ManyToManyField(Materials, related_name='material', verbose_name='venue', blank=True, null=True)
    equip_mreq=models.CharField(max_length=15 , verbose_name='Material Requirements' , choices=materials)
    equip_comm=models.TextField(max_length=2000 , verbose_name='comments')
	
class Fac_Trans(models.Model):
    user=models.ForeignKey(User, related_name='user_trans', blank=True)
    phone=models.FloatField()
    trans_bdate=models.DateField(default=now , verbose_name='pickup date')
    trans_jname=models.CharField(max_length=30 , verbose_name='Name of Judge/Artist')
    trans_noppl=models.IntegerField(max_length=3 , verbose_name='No. of people')
    trans_bpicloc=models.CharField(max_length=30 , verbose_name='pickup location')
    trans_btime=models.TimeField(default=now , verbose_name='pickup time')
    trans_bdes=models.CharField(max_length=30 , verbose_name='destination')
    trans_atime=models.TimeField(default=now , verbose_name='departure time')
    trans_adroloc=models.CharField(max_length=30 , verbose_name='departure location')
    trans_ades=models.CharField(max_length=15 , verbose_name='departure destination')
    
		
class user(models.Model):
    user=models.CharField(max_length=30)
    phone=models.FloatField()	

		

