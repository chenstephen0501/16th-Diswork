from django.db import models
from django.utils import timezone


class myEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class my_event(models.Model):
    summary = models.CharField(max_length=100, default="")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    description = models.TextField(default="")
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = myEventManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
