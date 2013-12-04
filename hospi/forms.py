from django import forms

from models import Hostel, Room
from events.models import Team

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['occupants']