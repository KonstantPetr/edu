from django.apps import AppConfig


class BoardingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boarding'

    def ready(self):
        import boarding.signals
