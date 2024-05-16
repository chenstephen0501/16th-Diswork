from django.db import models
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    vip_user = models.CharField(max_length=50, default="")
    vip_date_expiry = models.DateTimeField(null=True, blank=True)
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
