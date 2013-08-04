#From Django
from django import forms

#From models
from models import Task, Comment

# Form field over rides
forms.DateInput.input_type="date"

class AddTaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['destin_dept', 'title', 'summary', 'description', 'attachment', 'origin_deadline', 'origin_priority']

class OriginCoreApprovalForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(OriginCoreApprovalForm, self).__init__(*args, **kwargs)
		for f in ['destin_dept', 'title', 'summary', 'description', 'attachment', 'origin_deadline', 'origin_priority']:
			pass
			#Disable these fields using css
			#self.fields[f].widget.attrs['disabled'] = ''
			#self.fields[f].widget.attrs['class'] = 'input-xlarge disabled'
	class Meta:
		model = Task
		fields = ['destin_dept', 'title', 'summary', 'description', 'attachment', 'origin_deadline', 'origin_priority', 'origin_core_comment','origin_core_deadline', 'origin_core_priority', 'origin_core_assgnd_coord', 'origin_core_aproved']