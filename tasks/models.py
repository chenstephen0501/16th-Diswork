from typing import Any
from django.db import models
from django.utils import timezone

class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Task(models.Model):

    created_user = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    get_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    level = models.CharField(max_length=1, default='')

    objects = TaskManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

class TakeTask(models.Model):
    pass

class Situation(models.Model):
    col_name = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

