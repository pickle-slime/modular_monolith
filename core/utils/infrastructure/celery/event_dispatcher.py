from core.utils.infrastructure.celery import celery_app
from core.utils.exceptions import CeleryException
from core.utils.application.base_event import BaseACLEvent
import importlib

@celery_app.task(name="event_dispatcher", bind=True, max_retries=3)
def event_dispatcher(self, event_type: str, event_data: dict):
    try:
        module_path, class_name = event_type.rsplit(".", 1)
        module = importlib.import_module(module_path)    
        event_cls: type[BaseACLEvent] = getattr(module, class_name)

        event = event_cls(**event_data)
        handlers = celery_app.conf.event_handlers.get(event_type, [])
        
        for handler in handlers:
            handler(event)
    except CeleryException as ex:
        self.retry(exc=ex)

