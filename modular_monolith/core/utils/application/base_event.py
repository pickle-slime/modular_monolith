from typing import TypeVar
from pydantic import BaseModel

ACLEventType = TypeVar("ACLEventType", bound="BaseACLEvent")

class BaseACLEvent(BaseModel):
    pass
