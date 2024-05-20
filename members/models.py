from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    member_status = models.CharField(max_length=50, default="")
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)

    friends = models.ManyToManyField(
        "self", through="Friend", symmetrical=False, related_name="related_to"
    )  # symmetrical=False：設定兩者好友關係不是自動對稱的


class Status(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="statuses"
    )
    plan = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class Friend(models.Model):
    from_member = models.ForeignKey(
        Member, related_name="friend_requests_sent", on_delete=models.CASCADE
    )
    to_member = models.ForeignKey(
        Member, related_name="friend_requests_received", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("等待確認", "等待確認"),
            ("確認", "確認"),
            ("拒絕", "拒絕"),
        ],
        default="等待確認",
    )
    deleted_at = models.DateTimeField(null=True)
