from django import forms
from django.forms import widgets
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "picture"]
        labels = {"title": "標題", "content": "內容", "picture": "文章圖片"}
