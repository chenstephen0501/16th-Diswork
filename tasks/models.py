from django.db import models
from django.utils import timezone
from django.conf import settings

class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Task(models.Model):
    created_user = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    get_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    level = models.CharField(max_length=1, default="")
    situations_m2m = models.ManyToManyField("Situation", through="TakeTask")
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    objects = TaskManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

class Situation(models.Model):
    col_name = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tasks_m2m = models.ManyToManyField("Task", through="TakeTask")

class TakeTask(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, default=1)
    situation = models.ForeignKey("Situation", on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)