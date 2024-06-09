from django.db import models
from members.models import Member


class Notification(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
