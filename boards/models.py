from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from lib.softdelete import SoftDeleteable


class Category(SoftDeleteable, models.Model):
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
    member = models.ForeignKey(
        "members.Member", on_delete=models.CASCADE, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.picture:
            img = Image.open(self.picture)
            max_size = (400, 400)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()
            img_format = "PNG" if img.mode == "RGBA" else "JPEG"
            if img_format == "JPEG":
                img.save(thumb_io, format=img_format, quality=85)
            else:
                img.save(thumb_io, format=img_format)
            thumb_io.seek(0)
            file_extension = "png" if img.mode == "RGBA" else "jpg"
            new_file_name = f"{self.picture.name.split('.')[0]}_thumb.{file_extension}"
            self.picture.save(new_file_name, ContentFile(thumb_io.read()), save=False)

        super().save(*args, **kwargs)
