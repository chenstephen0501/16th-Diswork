from django.db import models
from django.utils import timezone


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Category(models.Model):
    title = models.CharField(max_length=50)
    rule = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("啟用", "啟用"),
            ("禁用", "禁用"),
        ],
        default="啟用",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")

    object = CategoryManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
