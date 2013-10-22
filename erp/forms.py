# From django
from django import forms
from django.contrib.auth.models import User


#From models
from models import Department
class UserLoginForm(forms.Form):
    '''
        Meant to be the Loginform at the Homepage, not implemented yet
        Currently dealt with a template login.html
    '''
    username=forms.CharField(help_text='Your username as registered with the ERP')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')
    
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department # Mentions the model
        
class AddUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise forms.ValidationError("this user exist already")

    def clean(self):
        try:
            if self.cleaned_data['password'] != self.cleaned_data['check_password']:
                raise forms.ValidationError("Passwords entered do not match")
        except KeyError:
      # didn't find what we expected in data - fields are blank on front end.  Fields
      # are required by default so we don't need to worry about validation
            pass
        return self.cleaned_data