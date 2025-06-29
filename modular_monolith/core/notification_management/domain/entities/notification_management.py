from core.notification_management.domain.entity import Entity
from core.notification_management.domain.value_objects.notification_management import CommonEmailField

from dataclasses import field
from datetime import datetime
import uuid

class NewsLetter(Entity):
    email: CommonEmailField | None = field(default=None)
    subscribed_at: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)
