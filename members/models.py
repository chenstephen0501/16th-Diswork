from django.db import models
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=50, default="")
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
    tasks = models.ManyToManyField("Task", through="MemberTask")


class Status(models.Model):
    plan = models.CharField(max_length=20, null=True, blank=True)
