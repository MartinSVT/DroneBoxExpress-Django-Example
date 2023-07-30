from django.apps import AppConfig


class OperationalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DroneBoxExpressApp.Operational'

    def ready(self):
        import DroneBoxExpressApp.Operational.signals
