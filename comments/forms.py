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
                    "class": "border border-gray-300 h-20 w-full p-2",
                    "placeholder": "這邊留言...",
                }
            ),
        }
