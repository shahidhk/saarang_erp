from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User, Group
#from erp.models import Department
#from events.models import Events
import datetime
now=datetime.datetime.now()
date=now.strftime("%Y-%m-%d")

class user(models.Model):
	name=models.CharField(max_length=15)
	password=models.CharField(max_length=15)
	
class facilities(models.Model):
	materials=(
		('sci', 'Scissors'),
		('ch' , 'Chairs'),
		('tab' , 'Tables'),
		)
	user=models.CharField(max_length=30)
	phone=models.FloatField()
	ip_date=models.DateField(default = date , verbose_name='date')
	ip_time=models.TimeField(default = now , verbose_name='time')
	ip_copies=models.IntegerField(max_length=5 , verbose_name='no. of copies')
	ven_date=models.DateField(default=date , verbose_name='date')
	ven_time=models.TimeField(default=now , verbose_name='time')
	ven_wifi=models.BooleanField(default=False , verbose_name='Wi-Fi')
	ven_ac=models.BooleanField(default=False , verbose_name='A/C')
	ven_foot=models.IntegerField(max_length=5)
	ven_sugg=models.CharField(max_length=15)
	ven_comments=models.TextField(max_length=2000)
	equip_date=models.DateField(default=date , verbose_name='date')
	equip_time=models.TimeField(default=now , verbose_name='time')
	equip_ven=models.CharField(max_length=15, verbose_name='venue')
	equip_mreq=models.CharField(max_length=15 , verbose_name='Material Requirements' , choices=materials)
	equip_comm=models.TextField(max_length=2000 , verbose_name='comments')
	trans_bdate=models.DateField(default=now , verbose_name='pickup date')
	trans_jname=models.CharField(max_length=30 , verbose_name='Name of Judge/Artist')
	trans_noppl=models.IntegerField(max_length=3 , verbose_name='No. of people')
	trans_bpicloc=models.CharField(max_length=30 , verbose_name='pickup location')
	trans_btime=models.TimeField(default=now , verbose_name='pickup time')
	trans_bdes=models.CharField(max_length=30 , verbose_name='destination')
	trans_atime=models.TimeField(default=now , verbose_name='departure time')
	trans_adroloc=models.CharField(max_length=30 , verbose_name='departure location')
	trans_ades=models.CharField(max_length=15 , verbose_name='departure destination')
		
		

		

