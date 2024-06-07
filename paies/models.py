from django.db import models
from members.models import Member
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Paies(models.Model):
    order = models.CharField(max_length=255, unique=True)
    amount = models.FloatField()
    status = models.CharField(max_length=255, null=True, default="PENDING")
    paid_at = models.CharField(max_length=255, null=True, default=None)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="members")
    merchant_id = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=50, null=True)
    item_desc = models.TextField(null=True)
    return_url = models.URLField(null=True)
    notify_url = models.URLField(null=True)