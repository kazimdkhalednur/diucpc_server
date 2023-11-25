from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from .utils import convert_title_to_slug


class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to="blog/", blank=True, null=True)
    description = RichTextUploadingField(blank=True)
    BLOG_STATUS = (("draft", "draft"), ("published", "published"))
    status = models.CharField(max_length=20, choices=BLOG_STATUS, default="draft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = convert_title_to_slug(self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)
