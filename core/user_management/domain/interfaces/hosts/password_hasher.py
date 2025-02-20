from abc import abstractmethod

from .....utils.domain.interfaces.hosts.base_host import BaseHost

class PasswordHasherHost(BaseHost):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        pass