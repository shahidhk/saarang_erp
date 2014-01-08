from django import forms
from models import SaarangUser

class SaarangUserForm(forms.ModelForm):
    class Meta:
        model = SaarangUser
        exclude = ['last_login', 'saarang_id', 'friend_list', 'fb_token', 'activate_status', 'fb_id', 'accomod_is_confirmed', 'password', 'college_id']
    # def __init__(self, *args, **kwargs):
    #     super(SaarangUserForm, self).__init__(*args, **kwargs)
    #     self.fields['desk_id'].widget.attrs['rel'] = "3"
    #     self.fields['gender'].widget.attrs['rel'] = "4"
    #     self.fields['email'].widget.attrs['rel'] = "5"
    #     self.fields['name'].widget.attrs['rel'] = "6"
    #     self.fields['mobile'].widget.attrs['rel'] = "7"
    #     self.fields['college_id'].widget.attrs['rel'] = "8"
    #     self.fields['college'].widget.attrs['rel'] = "9"