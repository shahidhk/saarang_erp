from django import forms
from models import SaarangUser

class SaarangUserForm(forms.ModelForm):
    class Meta:
        model = SaarangUser
        exclude = ['last_login', 'saarang_id', 'friend_list', 'fb_token', 'activate_status', 'fb_id', 'accomod_is_confirmed', 'password']