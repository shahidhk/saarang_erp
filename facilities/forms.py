from django import forms
from facilities.models import facilities

class ip(forms.ModelForm):
	class Meta:
		model=facilities
		fields= [ 'user' , 'phone' , 'ip_date' , 'ip_time' , 'ip_copies' ]
		
class venue(forms.ModelForm):
	class Meta:
		model=facilities
		fields=[ 'user' , 'ven_date' , 'ven_time' , 'ven_date' , 'ven_wifi' , 'ven_ac' , 'ven_foot' , 'ven_sugg' , 				'ven_comments']
	
class equipment(forms.ModelForm):
	class Meta:
		model=facilities
		fields=[ 'user' , 'equip_date' , 'equip_time' , 'equip_ven' , 'equip_mreq' , 'equip_comm']

class transport(forms.ModelForm):
	class Meta:
		model=facilities
		fields=[ 'user' , 'trans_bdate' , 'trans_jname' , 'trans_noppl' , 'trans_bpicloc' , 'trans_btime' , 				'trans_btime' , 'trans_bdes' , 'trans_atime' , 'trans_adroloc']


class Media:
	css={
		'all' : ('layout.css',)
		}
			
