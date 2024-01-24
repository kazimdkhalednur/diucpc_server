from django.apps import AppConfig


class CommitteesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diucpc.committees"

    def ready(self):
        from . import signals  # noqa: F401
