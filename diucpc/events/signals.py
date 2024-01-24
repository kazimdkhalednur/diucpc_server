from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Event
from .utils import convert_title_to_slug


@receiver(pre_save, sender=Event)
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


@receiver(pre_save, sender=Event)
def update_slug(sender, instance, **kwargs):
    # create the slug if it's not
    if not instance.slug:
        instance.slug = convert_title_to_slug(instance)

    # Update the slug only if the title has changed
    if instance.id:
        if instance.title != Event.objects.get(id=instance.id).title:
            instance.slug = convert_title_to_slug(instance)
