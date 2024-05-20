from django.db import models
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    member_status = models.CharField(max_length=50, default="")
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
    tasks = models.ManyToManyField("Task", through="MemberTask")
    friends = models.ManyToManyField("self")


class Status(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
    )
    plan = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True)


class Friend(models.Model):
    from_member = models.ForeignKey(
        Member, related_name="from_member", on_delete=models.CASCADE
    )
    to_member = models.ForeignKey(
        Member, related_name="to_member", on_delete=models.CASCADE
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
