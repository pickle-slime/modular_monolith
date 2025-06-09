from core.user_management.domain.events.events import NewUserDomainEvent
from core.utils.application.base_event import BaseACLEvent

import uuid

class NewUserACLEvent(BaseACLEvent):
    pub_uuid: uuid.UUID

    @classmethod
    def from_domain_event(cls, event: NewUserDomainEvent) -> 'NewUserACLEvent':
        return cls(
            pub_uuid=event.pub_uuid,
        )

class UserLoggedInACLEvent(BaseACLEvent):
    pub_uuid: uuid.UUID

