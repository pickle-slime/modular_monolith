from pydantic import BaseModel, Field
import uuid

from core.user_management.application.events.acl_events import UserLoggedInACLEvent

class LoggedUserEventDTO(BaseModel):
    pub_uuid: uuid.UUID = Field(description="User's public uuid")

    @classmethod
    def from_event(cls, event: UserLoggedInACLEvent) -> "LoggedUserEventDTO":
        return cls(
                pub_uuid=event.pub_uuid
            )

