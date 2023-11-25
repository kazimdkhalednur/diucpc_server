from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old_img = instance.__class__.objects.get(id=instance.id).profile_photo.path
        try:
            new_img = instance.profile_photo.path
        except ValueError:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except (ValueError, User.DoesNotExist):
        pass
