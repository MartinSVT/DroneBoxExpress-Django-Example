from django.apps import AppConfig


class UseraccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DroneBoxExpressApp.UserAccount'

    def ready(self):
        import DroneBoxExpressApp.UserAccount.signals
