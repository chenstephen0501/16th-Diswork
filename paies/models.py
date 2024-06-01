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
