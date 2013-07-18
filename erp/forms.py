# From django
from django import forms

class UserLoginForm(forms.Form):
	'''
		Meant to be the Loginform at the Homepage, not implemented yet
		Currently dealt with a template login.html
	'''
	username=forms.CharField(help_text='Your username as registered with the ERP')
	password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')