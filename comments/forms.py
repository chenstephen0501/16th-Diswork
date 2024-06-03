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
            "member": forms.TextInput(
                attrs={
                    "class": "hidden mx-1 h-12 focus:outline-none",
                    "readonly": "readonly",
                }
            ),
            "member": forms.TextInput(
                attrs={
                    "class": "invisible mx-1 border-2 border-gray-300 w-full",
                    "readonly": "readonly",
                }
            ),
        }
