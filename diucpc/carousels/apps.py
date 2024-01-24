from django.apps import AppConfig


class CarouselsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diucpc.carousels"

    def ready(self):
        from . import signals  # noqa: F401
