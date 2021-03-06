# From django
from django import forms
from django.contrib.auth.models import Group
from django.forms.widgets import SelectMultiple

#From models
from models import Event, EventRegistration, Team, Slot

class CreateEventForm(forms.ModelForm):
    COORDS = [[coord.id, coord.first_name] for coord in Group.objects.get(name="coord").user_set.all()]
    coords = forms.MultipleChoiceField(choices=COORDS, required=False)
    coords.widget.attrs.update({'id': 'multiselect', 'placeholder': 'Select coordinators', 'style':'width:300px'})
    class Meta:
        model = Event
        fields = ['name', 'long_name', 'sub_dept','google_group', 'email','is_team']

class EventForm(forms.ModelForm):
    COORDS = [[coord.id, coord.first_name] for coord in Group.objects.get(name="coord").user_set.all()]
    coords = forms.MultipleChoiceField(choices=COORDS, required=False)
    coords.widget.attrs.update({'id': 'multiselect', 'placeholder': 'Select coordinators', 'style':'width:300px'})
    class Meta:
        model = Event
        fields = ['long_name','google_group','oneliner', 'email','is_team','registration_open','registration_close_date','is_active']

class EventRegistrationInfoForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['category','registration_info']

class IntroductionForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = Event
        fields = ['about']

class FormatForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = Event
        fields = ['event_format']

class FAQForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = Event
        fields = ['FAQs']

class PrizesForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = Event
        fields = ['prizes']

class EventRegistrationForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = EventRegistration

class EventRegistrationForm(forms.ModelForm):
    is_shown = forms.BooleanField(initial=True,label='Show')
    class Meta:
        model = EventRegistration
        exclude = ['score']

class ChangeScoreForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['score']

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['team_sid', 'checked_status', 'members', 'checked_in', 'checked_out', 'mattress_count', 'mattress_returned']
    def __init__(self, *args, **kwargs):
        super(AddTeamForm, self).__init__(*args, **kwargs)
        self.fields['members'].widget.attrs['id'] = "multiselect"
        self.fields['members'].widget.attrs['style'] = "width: 220px;"

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        exclude = ['timestamp', 'created_by', 'event']
    def __init__(self, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        self.fields['comments'].widget.attrs['class'] = "comments"
