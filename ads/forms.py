from django import forms
from .models import Ads


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ["title", "picture", "url"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-1 w-full focus:outline-none focus:ring-2 focus:ring-gray-600",
                    "placeholder": "新增廣告商...",
                    "style": "font-size: 0.8em;",
                },
            ),
            "url": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-1 w-full focus:outline-none focus:ring-2 focus:ring-gray-600",
                    "placeholder": "新增網址...",
                    "style": "font-size: 0.8em;",
                },
            ),
            "picture": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-400 file:text-white hover:file:bg-[#3397cf]"
                },
            ),
        }
