from django import forms
from .models import Ads

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ["title", "picture", "url"]
