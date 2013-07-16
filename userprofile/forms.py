from django.forms import ModelForm
from models import UserProfile
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'post_count']