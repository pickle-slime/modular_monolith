from ...application.dtos.user_management import UserDTO

from abc import ABC, abstractmethod
import uuid

class IUserACL(ABC):
    @abstractmethod
    def fetch_by_uuid(self, inner_uuid: uuid.UUID | None = None, public_uuid: uuid.UUID | None = None) -> UserDTO:
        pass

    @abstractmethod
    def guest(self) -> UserDTO:
        pass
