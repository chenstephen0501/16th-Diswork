from django import forms
from .models import myEvent


class myEventForm(forms.ModelForm):
    class Meta:
        model = myEvent
        fields = ["summary", "start_time", "end_time", "description"]
        labels = {
            "summary": "活動",
            "start_time": "開始時間",
            "end_time": "結束時間",
            "description": "描述",
        }
