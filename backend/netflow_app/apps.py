from django.apps import AppConfig


class NetflowAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "netflow_app"

    def ready(self):
        import netflow_app.signals