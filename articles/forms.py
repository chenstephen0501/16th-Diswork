from django import forms
from django.forms import widgets
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "author", "content", "category"]
        labels = {
            "title": "標題",
            "author": "作者",
            "content": "內容",
            "category": "分類",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "text-black px-4 py-2 bg-transparent focus:outline-none", "readonly": "readonly"
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
        }
