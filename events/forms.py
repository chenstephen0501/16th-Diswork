from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["summary", "start_time", "end_time", "description"]
        labels = {
            "summary": "活動",
            "start_time": "開始時間",
            "end_time": "結束時間",
            "description": "描述",
        }
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
