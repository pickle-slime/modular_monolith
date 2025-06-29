from pydantic import BaseModel, Field
import uuid

from core.user_management.application.events.acl_events import NewUserACLEvent, UserLoggedInACLEvent

class LoggedUserEventDTO(BaseModel):
    pub_uuid: uuid.UUID = Field(description="User's public uuid")
    session_key: str = Field(description="User's session key, usually 8bit or 16bit hex")

    @classmethod
    def from_event(cls, event: UserLoggedInACLEvent) -> "LoggedUserEventDTO":
        return cls(
                pub_uuid=event.pub_uuid,
                session_key=event.session_key,
            )

class SignedUPUserEventDTO(BaseModel):
    pub_uuid: uuid.UUID = Field(description="User's public uuid")

    @classmethod
    def from_event(cls, event: NewUserACLEvent) -> "SignedUPUserEventDTO":
        return cls(
                pub_uuid=event.pub_uuid,
            )
