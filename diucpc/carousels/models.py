from django.db import models
from django.core.exceptions import ValidationError


class CarouselsManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)


class Carousels(models.Model):
    alt = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="carousels/")
    is_active = models.BooleanField(default=True)

    objects = CarouselsManager()

    def __str__(self):
        return self.image.name
    
    def clean(self) -> None:
        if not self.id and Carousels.objects.count() >= 5:
            raise ValidationError("You already 5 pics added")
    
    def save(self, *args, **kwargs):
        if not self.id and Carousels.objects.count() >= 5:
            raise ValidationError( "You already 5 pics added")
        super().save(*args, **kwargs)
