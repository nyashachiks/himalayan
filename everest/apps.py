from django.apps import AppConfig


class EverestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'everest'

    def ready(self):
        import everest.signals

