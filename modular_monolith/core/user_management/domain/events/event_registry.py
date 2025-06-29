from .events import DomainEventType

from contextlib import contextmanager
from typing import Iterator, Generic

class DomainEventRegistry(Generic[DomainEventType]):
    _events: list[DomainEventType] = list()

    @classmethod
    @contextmanager
    def scope(cls) -> Iterator[None]:
        original_events = cls._events
        cls._events = []
        try:
            yield
        finally:
            cls._events = original_events

    @classmethod
    def emit(cls, event: DomainEventType) -> None:
        cls._events.append(event)

    @classmethod
    def pop_events(cls) -> list[DomainEventType]:
        events = cls._events.copy()
        cls._events.clear()
        return events
