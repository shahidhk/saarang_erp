# From django
from django import forms

#From models
from models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event