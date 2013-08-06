#From Django
from django import forms

#From models
from models import Task, Comment

# Form field over rides
forms.DateInput.input_type="date"

class AddTaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['destin_dept', 'title', 'summary', 'description', 
				'attachment', 'origin_deadline', 'origin_priority']

class OriginCoreApprovalForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['origin_core_comment','origin_core_deadline', 
				'origin_core_priority', 'origin_core_assgnd_coord', 
				'origin_core_aproved']

class DestinCoreApprovalForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['destin_core_comment', 'destin_core_deadline', 
				'destin_core_priority', 'destin_core_assgnd_coord', 
				'destin_core_aproved']