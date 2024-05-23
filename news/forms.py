from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "url", "source", "published_at"]
        labels = {
            "title":"標題",
            "url":"新聞連結",
            "source":"來源",
            "published_at":"發布時間",
        }