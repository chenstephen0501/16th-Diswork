from django.forms import ModelForm
from .models import Comment
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": ""}
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "h-20 w-full p-2 pr-20 resize-none focus:outline-none",
                    "placeholder": "這邊留言...",
                }
            ),
        }
