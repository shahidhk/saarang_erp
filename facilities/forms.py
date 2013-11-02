from django import forms
from facilities.models import *

class Ip_form(forms.ModelForm):
	class Meta:
		model=Fac_Ip
		fields= [ 'phone' , 'ip_date' , 'ip_time' , 'ip_copies' ]
		
class Venue_form(forms.ModelForm):
	class Meta:
		model=Fac_Ven
		fields=[  'ven_date' , 'ven_time' , 'ven_date' , 'ven_wifi' , 'ven_ac' , 'ven_foot' , 'ven_sugg' , 'ven_comments']
	
class Equipment_form(forms.ModelForm):
	class Meta:
		model=Fac_Equip
		fields=[  'equip_date' , 'equip_time' , 'equip_ven' , 'equip_mreq' , 'equip_comm']

class Transport_form(forms.ModelForm):
	class Meta:
		model=Fac_Trans
		fields=[  'trans_bdate' , 'trans_jname' , 'trans_noppl' , 'trans_bpicloc' , 'trans_btime' , 'trans_btime' , 'trans_bdes' , 'trans_atime' , 'trans_adroloc']


class Media:
	css={
		'all' : ('layout.css',)
		}
			
