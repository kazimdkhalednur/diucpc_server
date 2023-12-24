from django.db import models


class Committee(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="committee/", null=True, blank=True)
    COMMITTEE_TYPE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )
    type = models.CharField(max_length=10, choices=COMMITTEE_TYPE_CHOICES)
    YEAR_CHOICES = ((str(i), str(i)) for i in range(2020, 2050))
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "year"], name="unique_committee")
        ]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)
