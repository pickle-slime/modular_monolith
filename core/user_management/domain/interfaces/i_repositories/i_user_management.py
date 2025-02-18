from .....utils.infrastructure.base_repository import BaseRepository
from core.user_management.domain.entities.user_management import User as UserEntity

from abc import abstractmethod
import uuid

class IUserRepository(BaseRepository):
    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity:
        pass

    @abstractmethod
    def find_by_uuid(self, inner_uuid: uuid.UUID = None, public_uuid: uuid.UUID = None) -> UserEntity:
        pass

    @abstractmethod
    def save(self, user: UserEntity) -> bool:
        pass