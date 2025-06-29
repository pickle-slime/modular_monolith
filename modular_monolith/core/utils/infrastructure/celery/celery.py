from __future__ import absolute_import, unicode_literals

import os

from core.utils.infrastructure.celery.event_subscriptions import register_event_handlers
from core.utils.infrastructure.adapters.event_bus import CeleryEventBusAdapter
from config import (
    CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER, CELERY_RESULT_SERIALIZER, CELERY_TIMEZONE, BOUNDED_CONTEXTS
)

from celery import Celery
import django

if os.environ.get("DEBUG_CELERY", "") == "1":
    import debugpy
    debugpy.listen(("127.0.0.1", 5678))
    print("Waiting for debugger to attach on port 5678...")
    debugpy.wait_for_client()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.presentation.electro.settings')
django.setup()
            
app = Celery(
    'electro',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    accept_content=CELERY_ACCEPT_CONTENT,
    task_serializer=CELERY_TASK_SERIALIZER,
    result_serializer=CELERY_RESULT_SERIALIZER,
    timezone=CELERY_TIMEZONE,     
)
            
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True 
            
bounded_contexts = BOUNDED_CONTEXTS.copy()
bounded_contexts.append("utils")
            
task_packages = []
for bc in bounded_contexts:
    path = "core/" + bc + "/infrastructure/celery"
    if os.path.exists(path) and os.path.isdir(path):
        module_path = "core." + bc + ".infrastructure.celery"
        task_packages.append(module_path)
            
app.autodiscover_tasks(packages=task_packages, related_name="event_dispatcher")
            
bus = CeleryEventBusAdapter(celery_app=app)
register_event_handlers(bus)

#app.conf.beat_schedule = {
#    'send-monthly-email-task': {
#        'task': 'notification_management.tasks.send_email_monthly_task',
#        'schedule': crontab(day_of_month=1, hour=0, minute=0),
#        'args': ('Monthly Update', 'electro@gmail.com', MAILCHIMP_AUDIENCE_ID, "<h1>Hello!</h1><p>This is a test email sent via Mailchimp.</p>"),
#    },
#}
