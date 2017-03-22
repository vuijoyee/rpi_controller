from django.apps import AppConfig


class V1Config(AppConfig):
    name = 'v1'

    def ready(self):
        import api.v1.signals
