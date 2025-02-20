from .base_host import BaseHost

from abc import abstractmethod

from typing import Any

class RedisHost(BaseHost):
    @abstractmethod
    def __init__(self, redis_url: str = 'redis://127.0.0.1:6379/0'):
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value, expire: int = None):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass


class RedisSessionHost(BaseHost):
    @abstractmethod
    def __init__(self, redis_adapter: RedisHost, session_key: str):
        pass

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set(self, data, expire: int = None):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def pop(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def _get_session_key(self) -> str:
        pass