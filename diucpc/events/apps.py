from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diucpc.events"

    def ready(self):
        from . import signals  # noqa: F401
