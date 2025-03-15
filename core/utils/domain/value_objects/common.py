from core.exceptions import InvalidForeignUUIDException

from dataclasses import dataclass, field
import uuid
import re


@dataclass(frozen=True)
class CommonNameField:
    value: str = field(default="")

    def __post_init__(self):
        if len(self.value) > 225:
            raise ValueError(f"{self.__class__.__name__}: max length of Brand is 225 symbols")
        
    def __str__(self):
        return self.value
        
@dataclass(frozen=True)
class CommonSlugField:
    value: str = field(default="")
    _slug_pattern: str = r"[!@#$%^&*(){}[]|~`,;:'\"<>?/] "

    def __post_init__(self):
        if len(self.value) > 225:
            raise ValueError(f"{self.__class__.__name__}: max length of name is 225 symbols")
        elif bool(re.search(self._slug_pattern, self.value)):
            raise ValueError(f"{self.__class__.__name__}: Incorrect slug")
        
    def __str__(self):
        return self.value
    
@dataclass(frozen=True)
class ForeignUUID:
    inner_uuid: uuid.UUID = field(default=None)
    public_uuid: uuid.UUID = field(default=None)

    def __post_init__(self):
        if self.inner_uuid is not None and not isinstance(self.inner_uuid, uuid.UUID):
            raise InvalidForeignUUIDException(
                f"{self.__class__.__name__}: inner_uuid is not a valid UUID object. "
                f"Received inner_uuid={type(self.inner_uuid)}."
            )
        
        if self.public_uuid is not None and not isinstance(self.public_uuid, uuid.UUID):
            raise InvalidForeignUUIDException(
                f"{self.__class__.__name__}: public_uuid is not a valid UUID object. "
                f"Received public_uuid={type(self.public_uuid)}."
            )
        
    def to_dict(self):
        return {
            "inner_uuid": self.inner_uuid,
            "public_uuid": self.public_uuid,
        }