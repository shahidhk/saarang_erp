# From django
from django import forms

#From models
from models import Event

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'long_name', 'sub_dept','google_group']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['long_name','google_group','oneliner']

class EventRegistrationForm(forms.ModelForm):
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