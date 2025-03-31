from ...infrastructure.repositories.user_management import DjangoUserRepository
from ..dtos.user_management import UserDTO
from ...domain.interfaces.i_acls import IUserACL
from core.user_management.domain.entities.user_management import User as UserEntity

import uuid

class UserACL(IUserACL):
    def __init__(self, user_repository: DjangoUserRepository):
        self.user_rep = user_repository

    def fetch_by_uuid(self, inner_uuid: uuid.UUID | None = None, public_uuid: uuid.UUID | None = None) -> UserDTO:
        return UserDTO.from_entity(self.user_rep.find_by_uuid(inner_uuid=inner_uuid, public_uuid=public_uuid))
    
    def guest(self) -> UserDTO:
        return UserDTO.from_entity(UserEntity.guest())
