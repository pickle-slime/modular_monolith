from core.utils.domain.interfaces.hosts.event_bus import CeleryEventBusHost
from core.utils.application.base_event import ACLEventType
from core.utils.exceptions import MissingCeleryAppException

from threading import Lock
from celery import Celery
from typing import Callable, Generic, Optional, ClassVar

class CeleryEventBusAdapter(CeleryEventBusHost, Generic[ACLEventType]):
    _instance: ClassVar[Optional['CeleryEventBusAdapter']] = None
    _lock: ClassVar[Lock] = Lock()
    _celery: Celery | None = None

    def __init__(self, celery_app: Celery | None = None):
        ...

    def __new__(cls, celery_app: Celery | None = None, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                if isinstance(celery_app, Celery):
                    cls._celery = celery_app
                else:
                    raise MissingCeleryAppException("celery_app must be provided on first initialization")
        return cls._instance
    
    @property
    def celery(self) -> Celery:
        if self._celery is None:
            raise MissingCeleryAppException("Celery app has not been initialized.")
        return self._celery

    def publish(self, event: ACLEventType):
        '''Publish event to Celery'''
        event_type = f"{event.__class__.__module__}.{event.__class__.__name__}"
        self.celery.send_task(
            name="event_dispatcher",
            kwargs={
                "event_type": event_type,
                "event_data": event.model_dump(),
            }
        )

    def subscribe(self, event_cls: type[ACLEventType], event_handler: Callable):
        '''Register event handler name for event type'''
        if not hasattr(self.celery.conf, "event_handlers"):
            self.celery.conf.event_handlers = {}

        key = f"{event_cls.__module__}.{event_cls.__name__}"
        self.celery.conf.event_handlers.setdefault(key, []).append(event_handler)
