from .base_host import BaseHost
from config import SESSIONS_EXPIRY

from abc import abstractmethod

from typing import Any

class RedisHost(BaseHost):
    @abstractmethod
    def __init__(self, redis_url: str = 'redis://127.0.0.1:6379/0'):
        pass

    @abstractmethod
    def hget(self, hash_name: str, key: str):
        pass

    @abstractmethod
    def hset(self, hash_name: str, key: str, value, expire: int = None):
        pass

    @abstractmethod
    def hdel(self, hash_name: str, key: str):
        pass

    @abstractmethod
    def expire(self, hash_name: str, expire: int):
        pass


class RedisSessionHost(BaseHost):
    @abstractmethod
    def __init__(self, session_key: str | None = None):
        pass

    @abstractmethod
    def hand_over_session_key(self, session_key: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, data: Any, expire: int = SESSIONS_EXPIRY):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def pop(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def _get_session_key(self) -> str:
        pass

    @abstractmethod
    def cache_key(self, key: str, prefix: str = "cache") -> str:
        pass