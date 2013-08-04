#From Django
from django import forms

#From models
from models import Task, Comment

# Form field over rides
forms.DateInput.input_type="date"

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['destin_dept', 'title', 'summary', 'description', 'attachment', 'origin_deadline']