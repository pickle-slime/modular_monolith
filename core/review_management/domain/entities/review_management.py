from core.review_management.domain.entity import Entity

from dataclasses import dataclass, field
from typing import TypeVar, Any
from datetime import datetime
import uuid

@dataclass(kw_only=True)
class Review(Entity):
    text: str | None = field(default=None)
    rating: int | None= field(default=None)
    date_created: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    @classmethod
    def map(cls, raw_data: dict[str, Any]) -> 'Review':
        return cls(
                text=raw_data.get("text", None),
                rating=raw_data.get("rating", None),
                date_created=raw_data.get("date_created", None),
                user=raw_data.get("user", None)
            )


ReviewEntityType = TypeVar("ReviewEntityType", bound=Review)
