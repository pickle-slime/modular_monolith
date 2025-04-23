from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository
from core.user_management.domain.entities.user_management import User as UserEntity

from abc import abstractmethod
import uuid

class IUserRepository(BaseRepository):
    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity:
        pass

    @abstractmethod
    def find_by_uuid(self, inner_uuid: uuid.UUID | None = None, public_uuid: uuid.UUID | None = None) -> UserEntity:
        pass

    @abstractmethod
    def save(self, user: UserEntity) -> tuple[UserEntity, bool]:
        pass

    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        pass

