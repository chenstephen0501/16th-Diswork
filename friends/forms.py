from django import forms
from .models import Friend


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ["from_member", "status"]
        labels = {
            "from_member": "好友邀請",
            "status": "等待中",
        }
