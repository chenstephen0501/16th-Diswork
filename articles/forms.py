from django import forms
from django.forms import widgets
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "picture"]
        labels = {"title": "標題", "content": "內容", "picture": "文章圖片"}
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border border-gray-300 text-black rounded-md px-4 py-1 w-full focus:outline-none focus:ring-2 focus:ring-gray-600"
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "peer h-full min-h-[220px] w-full resize-none rounded-[7px] border border-blue-gray-200 border-t-transparent bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 outline outline-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:resize-none disabled:border-0 disabled:bg-blue-gray-50 bg-white",
                    "placeholder": "",
                    "style": "height: 100px",
                },
            ),
            "picture": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100"
                },
            ),
        }
