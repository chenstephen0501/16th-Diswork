from django.utils import timezone
from django.conf import settings
from django.db import models

class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Task(models.Model):
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField(default="")
    urgency = models.CharField(max_length=1, default="", choices=[("高", "高"), ("中", "中"), ("低", "低")])
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    situation = models.ForeignKey("Situation", on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="MemberTask", related_name='assigned_tasks')
    deleted_at = models.DateTimeField(null=True)
    objects = TaskManager()
    
    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
        
    def __str__(self):
        return self.title

class Situation(models.Model):
    col_name = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.col_name

class MemberTask(models.Model):
    tasks = models.ForeignKey("Task", on_delete=models.CASCADE, default=1)
    members = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.member}, {self.task}"