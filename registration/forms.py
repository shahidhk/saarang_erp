from django import forms

from models import SaarangUser

class SaarangUserForm(forms.ModelForm):
    class Meta:
        model = SaarangUser
        exclude = ['saarang_id', 'friend_list', 'fb_token', 'activate_status']