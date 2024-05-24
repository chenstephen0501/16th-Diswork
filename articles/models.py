from django.db import models
from django.conf import settings
from django.utils import timezone

class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Article(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    like_article = models.ManyToManyField(settings.AUTH_USER_MODEL, through="LikeArticle", related_name="like_article")

    objects = ArticleManager()

    def __str__(self):
        return f"123{self.title}"

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class LikeArticle(models.Model):
    like_article = models.ForeignKey("Article", related_name="article", on_delete=models.CASCADE)
    like_by_article = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="like_by_article", on_delete=models.CASCADE)