from django.forms import ModelForm
from .models import Comment
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "member"]
        labels = {
            "content": "留言內容",
            "member": "會員",
        }
        widgets = {
            "content": forms.TextInput(
                attrs={"class": "mx-1 border-2 border-gray-300 h-32 w-full"}
            ),
            "member": forms.TextInput(
                attrs={"class": "invisible mx-1 h-12 focus:outline-none", "readonly": "readonly",}
            ),
        }

