from core.utils.domain.entity import Entity
from core.utils.domain.value_objects.common import CommonEmailField

from dataclasses import field
from datetime import datetime
import uuid

class NewsLetter(Entity):
    email: CommonEmailField | None = field(default=None)
    subscribed_at: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)
