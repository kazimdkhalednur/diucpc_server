from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import profile_photo_path


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(
        upload_to=profile_photo_path, blank=True, null=True
    )
    USER_ROLE = (
        ("general", "General"),
        ("associative", "Associative"),
        ("executive", "Executive"),
        ("core", "Core"),
    )
    role = models.CharField(max_length=20, choices=USER_ROLE, default="general")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email
