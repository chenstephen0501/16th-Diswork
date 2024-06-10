from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Member(AbstractUser):
    name = models.CharField(max_length=100, default="")
    member_status = models.CharField(max_length=50, default="")
    user_img = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
    tasks = models.ManyToManyField("tasks.Task", through="tasks.MemberTask")
    friends = models.ManyToManyField(
        "self", through="friends.Friend", symmetrical=False, related_name="related_to"
    )  # symmetrical=False：設定兩者好友關係不是自動對稱的
    like_by = models.ManyToManyField(
        "comments.Comment", through="comments.LikeComment", related_name="like_sender"
    )

    liking_article_members = models.ManyToManyField(
        "articles.Article",
        through="articles.LikeArticle",
        related_name="liking_article_members",
    )
    cards = models.ManyToManyField("self", through="friends.Card", symmetrical=False, related_name="related_to_card")
    
    birthday = models.DateField(null=True, blank=True)
    interest = models.TextField(null=True, blank=True)
    constellation = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user_img:
            img = Image.open(self.user_img)
            if img.mode == "P":
                img = img.convert("RGB")
            max_size = (200, 200)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()
            img_format = "PNG" if img.mode == "RGBA" else "JPEG"
            img.save(thumb_io, format=img_format)
            thumb_io.seek(0)
            file_extension = "png" if img.mode == "RGBA" else "jpg"
            new_file_name = f"{self.user_img.name.split('.')[0]}_thumb.{file_extension}"
            self.user_img.save(new_file_name, ContentFile(thumb_io.read()), save=False)
        super().save(*args, **kwargs)


class Status(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="statuses"
    )
    plan = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True)
