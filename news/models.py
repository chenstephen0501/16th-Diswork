from django.db import models
from django.utils import timezone
from lib.softdelete import SoftDeleteable


class News(SoftDeleteable, models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=1024)
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
