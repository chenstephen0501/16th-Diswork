from django.db import models
from django.conf import settings
from django.utils import timezone


class FriendManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Friend(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_friends",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_friends",
        on_delete=models.CASCADE,
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

    objects = FriendManager()

    def get_friends(self):
        sent_friends = Friend.objects.filter(sender=self.sender, deleted_at=None)
        received_friends = Friend.objects.filter(receiver=self.sender, deleted_at=None)
        return sent_friends | received_friends

    def get_how_many_friends(self):
        return self.get_friends().count()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
