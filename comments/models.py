from django.db import models
from django.utils import timezone
from django.conf import settings
from articles.models import Article
from lib.softdelete import SoftDeleteable


class Comment(SoftDeleteable, models.Model):
    member = models.ForeignKey("members.Member", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, default="", related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    like_comment = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="LikeComment", related_name="like_comment"
    )


class LikeComment(models.Model):
    like_comment = models.ForeignKey(
        "Comment", related_name="comment", on_delete=models.CASCADE
    )
    like_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sender", on_delete=models.CASCADE
    )
