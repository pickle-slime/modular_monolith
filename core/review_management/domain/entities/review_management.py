from core.utils.domain.entity import Entity

from dataclasses import dataclass, field
from typing import TypeVar
from datetime import datetime
import uuid

@dataclass(kw_only=True)
class Review(Entity):
    text: str | None = field(default=None)
    rating: int | None= field(default=None)
    date_created: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

ReviewEntityType = TypeVar("ReviewEntityType", bound=Review)
