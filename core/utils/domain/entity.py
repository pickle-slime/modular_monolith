from typing import Any, TypeVar, Protocol
import uuid

EntityType = TypeVar("EntityType", covariant=True)

class Entity(Protocol[EntityType]):
    inner_uuid: uuid.UUID
    public_uuid: uuid.UUID

    def __eq__(self, other: Any) -> bool: ...

