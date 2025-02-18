from abc import abstractmethod

from .....utils.infrastructure.base_host import BaseHost

class PasswordHasherHost(BaseHost):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        pass