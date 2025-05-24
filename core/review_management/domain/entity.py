from dataclasses import dataclass, field, fields, is_dataclass
from typing import TypeVar, Any
import uuid

EntityType = TypeVar("EntityType", bound="Entity")

@dataclass(kw_only=True, init=False)
class Entity:
    inner_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    public_uuid: uuid.UUID = field(default_factory=uuid.uuid4)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.inner_uuid == other.inner_uuid
        else:
            return False

    @classmethod
    def require_fields(cls, *required_fields):
        def decorator(func):
            def wrapper(self, *args, **kwargs):

                if not is_dataclass(self):
                    raise TypeError("Provided object is not a dataclass instance")

                field_names = required_fields or {f.name for f in fields(self)}

                for name in field_names:
                    if getattr(self, name) is None:
                        raise ValueError(f"Field '{name}' is required for {func.__name__}")

                return func(self, *args, **kwargs)
            return wrapper
        return decorator
