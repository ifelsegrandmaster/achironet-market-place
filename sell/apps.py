from django.apps import AppConfig


class SellConfig(AppConfig):
    name = 'sell'

    def ready(self):
        import sell.signals
