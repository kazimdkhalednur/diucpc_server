from django.db import models

from .utils import committee_photo_path

class CommitteeManager(models.Manager):
    def student(self, **kwargs):
        return self.filter(type="student", **kwargs)
    
    def teacher(self, **kwargs):
        return self.filter(type="teacher", **kwargs)


class Committee(models.Model):
    class CommitteeType(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"

    thumbnail = models.ImageField(upload_to=committee_photo_path)
    type = models.CharField(max_length=10, choices=CommitteeType.choices)
    YEAR_CHOICES = ((str(i), str(i)) for i in range(2020, 2050))
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommitteeManager()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["type", "year"], name="unique_committee")
        ]

    def __str__(self):
        return f"{self.type} committee {self.year}"

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)
