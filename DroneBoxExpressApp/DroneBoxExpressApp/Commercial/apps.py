from django.apps import AppConfig


class CommercialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DroneBoxExpressApp.Commercial'

    def ready(self):
        import DroneBoxExpressApp.Commercial.signals
