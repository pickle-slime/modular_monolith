from django.apps import AppConfig
import sys

class UtilsAppConfig(AppConfig):
    name = 'core.utils.presentation.bootstrap'

    def ready(self):
        if "runserver" in sys.argv or "gunicorn" in sys.argv or "celery" in sys.argv:
            from core.utils.infrastructure.celery.celery import app
