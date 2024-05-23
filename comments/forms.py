from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content":"留言內容",
        }