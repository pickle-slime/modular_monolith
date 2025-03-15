from core.utils.domain.entity import Entity

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(kw_only=True)
class Review(Entity):
    text: str = field(default=None)
    rating: int = field(default=None)
    date_created: datetime = field(default=None)

    user: uuid.UUID = field(default=None)

    def format_date(self, format_str: str = "%d %B %Y, %-I:%M %p") -> str:
        return self.date_created.strftime(format_str)

