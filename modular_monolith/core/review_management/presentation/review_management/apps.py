from django.apps import AppConfig


class ReviewManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.review_management.presentation.review_management'

    def ready(self):
        import core.review_management.presentation.review_management.signals
