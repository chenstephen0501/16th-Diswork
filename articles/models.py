from django.db import models
from django.conf import settings
from django.utils import timezone
from boards.models import Category


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)
    
    def with_count(self):
        return self.get_queryset().annotate(
            like_count=models.Count('like_article', filter=models.Q(like_article__article__deleted_at__isnull=True), distinct=True),
            comment_count=models.Count('comments', filter=models.Q(comments__deleted_at__isnull=True), distinct=True)
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

    objects = ArticleManager()

    def __str__(self):
        return f"{self.title}"

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class LikeArticle(models.Model):
    like_article = models.ForeignKey(
        "Article", related_name="article", on_delete=models.CASCADE
    )
    like_by_article = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="like_by_article",
        on_delete=models.CASCADE,
    )
