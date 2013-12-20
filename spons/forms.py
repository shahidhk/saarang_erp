from models import SponsImageUpload
from django import forms

class AddLogoForm(forms.ModelForm):
    class Meta:
        model = SponsImageUpload
        exclude = ['timestamp']
        help_texts = {
            'title': ('Example:Title Sponsor, Website Sponsor'),
        }