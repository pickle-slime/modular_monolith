from core.utils.domain.events import BaseDomainEvent
from core.utils.infrastructure.celery.celery import app
from core.utils.exceptions import CeleryException
import importlib

@app.task(name="event_dispatcher", bind=True, max_retries=3)
def event_dispatcher(self, event_type: str, event_data: dict):
    try:
        module_path, class_name = event_type.rsplit(".", 1)
        module = importlib.import_module(module_path)    
        event_cls: BaseDomainEvent = getattr(module, class_name)

        event = event_cls.from_dict(event_data)
        handlers = app.conf.event_handlers.get(event_type, [])
        
        for handler in handlers:
            handler(event)
    except CeleryException as ex:
        self.retry(exc=ex)

