from django.apps import AppConfig


class XConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "x"

    def ready(self):
        import x.signals