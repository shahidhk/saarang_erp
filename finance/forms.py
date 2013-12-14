from django import forms
from django.contrib.auth.models import Group
from django.forms.widgets import SelectMultiple
from finance.models import Item,Memento 

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['count','timestamp']

class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['count','timestamp','cost']

class CreateMementoForm(forms.ModelForm):
    class Meta:
        model = Memento
        exclude = ['timestamp']

class FacilityForm(forms.Form):



class HospitalityForm(forms.Form):


class PPMForm(forms.Form):


class MiscellaneousForm(forms.Form):
