from core.utils.application.base_event import ACLEventType

from typing import Callable, Generic

class CeleryEventBusHost(Generic[ACLEventType]):
    def publish(self, event: ACLEventType): ...
    def subscribe(self, event_cls: type[ACLEventType], event_handler: Callable): ...

