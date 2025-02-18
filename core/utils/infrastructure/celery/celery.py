from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings
#from core.presentation.electro.settings import MAILCHIMP_AUDIENCE_ID

from celery import Celery
from celery.schedules import crontab

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electro.settings')

app = Celery('electro')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True 

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-monthly-email-task': {
        'task': 'notification_management.tasks.send_email_monthly_task',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
        'args': ('Monthly Update', 'electro@gmail.com', settings.MAILCHIMP_AUDIENCE_ID, "<h1>Hello!</h1><p>This is a test email sent via Mailchimp.</p>"),
    },
}
