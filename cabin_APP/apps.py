from django.apps import AppConfig


class CabinAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cabin_APP'

class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cabin_APP'

    def ready(self):
        import cabin_APP.signal
