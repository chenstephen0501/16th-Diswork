from django.db import models
from lib.softdelete import SoftDeleteable

class Ads(SoftDeleteable, models.Model):
    title = models.TextField()
    picture = models.ImageField(upload_to='ads/', verbose_name="picture")
    url = models.URLField(max_length=200, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)