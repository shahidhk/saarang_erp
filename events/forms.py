# From django
from django import forms
from django.contrib.auth.models import Group

#From models
from models import Event,EventRegistration

class CreateEventForm(forms.ModelForm):
    COORDS = [[coord.id, coord.first_name] for coord in Group.objects.get(name="coord").user_set.all()]
    coords = forms.MultipleChoiceField(choices=COORDS)
    class Meta:
        model = Event
        fields = ['name', 'long_name', 'sub_dept','google_group', 'email','is_team']

class EventForm(forms.ModelForm):
    COORDS = [[coord.id, coord.first_name] for coord in Group.objects.get(name="coord").user_set.all()]
    coords = forms.MultipleChoiceField(choices=COORDS, initial='39')
    class Meta:
        model = Event
        fields = ['long_name','google_group','oneliner', 'email','is_team','registration_open','registration_close_date']

class EventRegistrationInfoForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['category','registration_info']

class IntroductionForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['about']

class FormatForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['event_format']

class FAQForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['FAQs']

class PrizesForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['prizes']

class EventRegistrationForm(forms.ModelForm):
	class Meta:
		model = EventRegistration