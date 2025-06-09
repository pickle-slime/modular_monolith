from dataclasses import dataclass
from typing import TypeVar
import uuid

DomainEventType = TypeVar("DomainEventType", bound="BaseDomainEvent")

class BaseDomainEvent:
    pass

@dataclass(frozen=True)
class NewUserDomainEvent(BaseDomainEvent):
    pub_uuid: uuid.UUID
