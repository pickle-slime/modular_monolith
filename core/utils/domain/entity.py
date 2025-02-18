from dataclasses import dataclass, field
from typing import Any, TypeVar
import uuid

@dataclass(kw_only=True, init=False)
class Entity:
    inner_uuid: uuid.UUID | None = field(default_factory=uuid.uuid4)
    public_uuid: uuid.UUID | None = field(default_factory=uuid.uuid4)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.inner_uuid == other.inner_uuid
        else:
            return False

EntityType = TypeVar("EntityType", bound=Entity)

