from django.db import models
from django.utils import timezone


class myEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class myEvent(models.Model):
    summary = models.CharField(max_length=100, default="")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    description = models.TextField(default="")
    deleted_at = models.DateTimeField(null=True)

    objects = myEventManager()


def delete(self):
    self.deleted_at = timezone.now()
    self.save()
