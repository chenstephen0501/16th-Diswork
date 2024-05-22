from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    member_status = models.CharField(max_length=50, default="")
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
    tasks = models.ManyToManyField("tasks.Task", through="tasks.MemberTask")
    friends = models.ManyToManyField(
        "self", through="friends.Friend", symmetrical=False, related_name="related_to"
    )  # symmetrical=False：設定兩者好友關係不是自動對稱的
    like_by = models.ManyToManyField("comments.Comment", through="comments.LikeComment", related_name="like_sender")

    liking_article_mambers = models.ManyToManyField("articles.Article", through="articles.LikeArticle", related_name="liking_article_mambers")

class Status(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="statuses"
    )
    plan = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
