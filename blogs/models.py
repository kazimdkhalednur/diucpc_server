from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from .utils import convert_title_to_slug


class PublishedBlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to="blog/", blank=True, null=True)
    description = RichTextUploadingField(blank=True)
    BLOG_STATUS_CHOICES = (("draft", "draft"), ("published", "published"))
    status = models.CharField(
        max_length=20, choices=BLOG_STATUS_CHOICES, default="draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published_objects = PublishedBlogManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = convert_title_to_slug(self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)
