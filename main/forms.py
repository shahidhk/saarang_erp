from django import forms
from django.contrib.auth.models import Group
from django.forms.widgets import SelectMultiple
from main.validators import isalphavalidator

GENDER_CHOICES =['Male','Female']

class ProfileEditForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10,required=False,validators=[isalphavalidator], help_text='10 digit mobile number')
    gender = forms.ChoiceField(choices=(('Male', 'Male'),('Female', 'Female')))
    college = forms.CharField(max_length=200,required=False,help_text='Enter the name of your college if you are a student, None , if you are not.')

class CreateTeamForm(forms.Form):
    team_name = forms.CharField(max_length=200,label='Team Name',help_text="You will be the leader of the team")
    members = forms.CharField(max_length=5000,label='Email-IDs of the team members',help_text='Enter multiple Email-IDs seperated by a comma(,).The members should be registered, or else register at <a href="www.saarang.org">Saarang</a>.')

class EventOptionsForm(forms.Form):
    submission1 = forms.CharField(max_length=500,label='First Submission',required=False)
    submission2 = forms.CharField(max_length=500,label='Second Submission',required=False)    
    submission3 = forms.CharField(max_length=500,label='Third Submission',required=False)    
    band_email = forms.EmailField(label='Band Email Id',required=False,help_text='Please verify before submission')