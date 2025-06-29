from django.apps import AppConfig


class CartManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.cart_management.presentation.cart_management'

    def ready(self):
        import core.cart_management.presentation.cart_management.signals
