from ...domain.entities.user_management import User as UserEntity

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class UserDTO(BaseModel):
    uuid: UUID | None = Field(default=None)
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    date_joined: datetime | None = Field(default=None)
    last_login: datetime | None = Field(default=None)

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserDTO':
        return UserDTO(
            uuid=entity.public_uuid,
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            date_joined=entity.date_joined,
            last_login=entity.last_login,
        )