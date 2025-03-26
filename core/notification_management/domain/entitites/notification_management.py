from core.utils.domain.entity import Entity

from datetime import datetime
from dataclasses import field
import uuid

class NewsLetter(Entity):
    created_at: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)
