from core.user_management.domain.events.events import NewUserDomainEvent

from pydantic import BaseModel
import uuid

class NewUserAppEvent(BaseModel):
    pub_uuid: uuid.UUID

    @classmethod
    def from_domain_event(cls, event: NewUserDomainEvent) -> 'NewUserAppEvent':
        return cls(
            pub_uuid=event.pub_uuid,
        )
