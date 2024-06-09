from django.db import models
from django.conf import settings
from django.utils import timezone
from lib.softdelete import SoftDeleteable


class Friend(SoftDeleteable, models.Model):
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
        max_length=1,
        choices=[
            ("1", "等待確認"),
            ("2", "確認"),
            ("3", "拒絕"),
        ],
        default="1",
    )
    deleted_at = models.DateTimeField(null=True)


class Card(models.Model):
    drawer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="draw", on_delete=models.CASCADE)
    drawn = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="drawn", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)