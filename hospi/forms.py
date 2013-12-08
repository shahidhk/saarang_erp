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

class HospiTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['team_sid', 'checked_status', 'leader', 'accomodation_status']
    def __init__(self, *args, **kwargs):
        super(HospiTeamForm, self).__init__(*args, **kwargs)
        self.fields['members'].widget.attrs['id'] = "multiselect"
        self.fields['members'].widget.attrs['style'] = "width: 220px;"