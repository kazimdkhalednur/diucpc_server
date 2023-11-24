from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Event(models.Model):
    title = models.CharField(max_length=300)
    description = RichTextUploadingField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to="cover/", blank=True, null=True)
    started_date = models.DateField(blank=True, null=True)
    ended_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

