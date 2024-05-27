from django import forms
from django.forms import widgets
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
        labels = {
            "title": "標題",
            "content": "內容",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['readonly'] = True