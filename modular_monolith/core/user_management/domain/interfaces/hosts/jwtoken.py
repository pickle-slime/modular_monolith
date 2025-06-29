from abc import abstractmethod
from typing import Any
import uuid

from core.utils.domain.interfaces.hosts.base_host import BaseHost

class TokenHost(BaseHost):
    @abstractmethod
    def __init__(self, secret_key, access_token_expiry, refresh_token_expiry):
        pass

    @abstractmethod
    def generate_access_token(self, user_public_uuid: uuid.UUID) -> str:
        pass

    @abstractmethod
    def refresh_token(self, user_public_uuid: uuid.UUID) -> str:
        pass

    @abstractmethod
    def decode_token(self, token) -> Any:
        pass

    @abstractmethod
    def is_token_expired(self, token) -> bool:
        pass
