from django.apps import AppConfig


class ClientspaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientspace'

    def ready(self):
        import clientspace.signals