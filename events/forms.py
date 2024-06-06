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
            "summary": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "peer h-full min-h-[220px] w-full resize-none rounded-[7px] border border-blue-gray-200 border-t-transparent bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 outline outline-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:resize-none disabled:border-0 disabled:bg-blue-gray-50 bg-white",
                    "placeholder": "",
                    "style": "height: 100px",
                },
            ),
        }
