from __future__ import absolute_import, unicode_literals

from config import *
from core.utils.infrastructure.celery.event_subscriptions import register_event_handlers

from celery import Celery
from celery.schedules import crontab

app = Celery(
    'electro',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    accept_content=CELERY_ACCEPT_CONTENT,
    task_serializer=CELERY_TASK_SERIALIZER,
    result_serializer=CELERY_RESULT_SERIALIZER,
    timezone=CELERY_TIMEZONE,     
)

app.conf.broker_connection_retry_on_startup = True 

app.autodiscover_tasks()

register_event_handlers()

app.conf.beat_schedule = {
    'send-monthly-email-task': {
        'task': 'notification_management.tasks.send_email_monthly_task',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
        'args': ('Monthly Update', 'electro@gmail.com', MAILCHIMP_AUDIENCE_ID, "<h1>Hello!</h1><p>This is a test email sent via Mailchimp.</p>"),
    },
}
