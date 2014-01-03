from django import forms
from django.contrib.auth.models import Group
from django.forms.widgets import SelectMultiple
from finance.models import Item,Memento 

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['timestamp']

class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['count','timestamp','cost']

class CreateMementoForm(forms.ModelForm):
    class Meta:
        model = Memento
        exclude = ['timestamp']

# class CommentForm(forms.Form):
#     comment = forms.CharField(widget=SummernoteWidget())


# class HospitalityForm(forms.Form):


# class PPMForm(forms.Form):


# class MiscellaneousForm(forms.Form):
