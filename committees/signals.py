from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Committee


@receiver(pre_save, sender=Committee)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old_img = instance.__class__.objects.get(id=instance.id).thumbnail.path
        try:
            new_img = instance.thumbnail.path
        except:  # noqa : E722
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:  # noqa : E722
        pass
