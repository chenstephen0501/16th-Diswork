from django.db import models
from django.conf import settings
from django.utils import timezone
from boards.models import Category
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def with_count(self):
        return self.get_queryset().annotate(
            like_count=models.Count(
                "like_article",
                filter=models.Q(like_article__article__deleted_at__isnull=True),
                distinct=True,
            ),
            comment_count=models.Count(
                "comments",
                filter=models.Q(comments__deleted_at__isnull=True),
                distinct=True,
            ),
        )


class Article(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=""
    )
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    like_article = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="LikeArticle", related_name="like_article"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")

    objects = ArticleManager()

    def __str__(self):
        return f"{self.title}"

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.picture:
            img = Image.open(self.picture)
            max_size = (300, 300)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()
            img_format = "PNG" if img.mode == "RGBA" else "JPEG"
            img.save(thumb_io, format=img_format)
            thumb_io.seek(0)
            file_extension = "png" if img.mode == "RGBA" else "jpg"
            new_file_name = f"{self.picture.name.split(".")[0]}_thumb.{file_extension}"
            self.picture.save(new_file_name, ContentFile(thumb_io.read()), save=False)
        super().save(*args, **kwargs)

class LikeArticle(models.Model):
    like_article = models.ForeignKey(
        "Article", related_name="article", on_delete=models.CASCADE
    )
    like_by_article = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="like_by_article",
        on_delete=models.CASCADE,
    )
