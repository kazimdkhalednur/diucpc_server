from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from .utils import convert_title_to_slug


class EventManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status="published", **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Don't write anything in this field. It will automatically generate when you save this.",  # noqa: E501
    )
    thumbnail = models.ImageField(upload_to="cover/", blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    speaker_name = models.CharField(max_length=100)
    speaker_designation = models.TextField(blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    registration_note = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    started_date = models.DateField(blank=True, null=True)
    ended_date = models.DateField(blank=True, null=True)
    EVENT_STATUS = (("draft", "draft"), ("published", "published"))
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default="draft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()

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
