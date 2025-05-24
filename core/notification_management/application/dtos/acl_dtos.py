from core.notification_management.application.dtos.base_dto import BaseDTO

from core.user_management.application.dtos.user_management import UserDTO

from pydantic import Field, model_validator
import uuid

class ACLUserDTO(BaseDTO["ACLUserDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    username: str | None = Field(default=None, min_length=2, max_length=225, title="Username")
    email: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", min_length=2, max_length=100, title="Email")
    first_name: str | None = Field(default=None, min_length=2, max_length=225, title="First Name")
    last_name: str | None = Field(default=None, min_length=2, max_length=225, title="Last Name")
    role: str | None = Field(default=None, examples=["user", "guest", "admin"], title="Role")

    @model_validator(mode="before")
    def validate_pub_uuid(cls, values):
        role = values.get('role')
        if role == "guest":
            values['pub_uuid'] = None
        return values

    @staticmethod
    def from_user_dto(dto: UserDTO) -> 'ACLUserDTO':
        return ACLUserDTO(
            pub_uuid=dto.pub_uuid,
            username=dto.username,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            role=dto.role,
        )

