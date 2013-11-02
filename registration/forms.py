from django import forms

from models import SaarangUser

class SaarangUserForm(forms.ModelForm):
    class Meta:
        model = SaarangUser