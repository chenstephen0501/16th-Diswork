from django import forms
from django.forms import widgets
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "author", "content"]
        labels = {
            "title": "標題",
            "author": "作者",
            "content": "內容",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-400"},
            ),
            "content": forms.Textarea(
                attrs={"class": "block w-full rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-400"},
            ),
        }
