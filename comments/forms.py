from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "created_at"]
        label = {
            "content":"留言內容",
            "created_at":"時間",
        }