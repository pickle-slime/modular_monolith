from ...domain.entities.user_management import User as UserEntity

from core.utils.application.base_dto import BaseEntityDTO

from pydantic import Field, model_validator
import uuid
from datetime import datetime

class UserDTO(BaseEntityDTO["UserDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    username: str | None = Field(default=None, min_length=2, max_length=225, title="Username")
    email: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", min_length=2, max_length=100, title="Email")
    first_name: str | None = Field(default=None, min_length=2, max_length=225, title="First Name")
    last_name: str | None = Field(default=None, min_length=2, max_length=225, title="Last Name")
    date_joined: datetime | None = Field(default=None, title="Date joined")
    last_login: datetime | None = Field(default=None, title="Last Login")
    role: str | None = Field(default=None, examples=["user", "guest", "admin"], title="Role")

    @model_validator(mode="before")
    def validate_pub_uuid(cls, values):
        role = values.get('role')
        if role == "guest":
            values['pub_uuid'] = None
        return values

    @classmethod
    def from_entity(cls, entity: UserEntity) -> 'UserDTO':
        return cls(
            pub_uuid=entity.public_uuid,
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            date_joined=entity.date_joined,
            last_login=entity.last_login,
            role=entity.role,
        )

    @property
    def is_authenticated(self) -> bool:
        return self.role != "guest" and self.pub_uuid is not None
