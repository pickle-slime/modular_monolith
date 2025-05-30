from core.utils.domain.interfaces.hosts.redis import RedisHost, RedisSessionHost
from core.utils.domain.interfaces.hosts.serializer import SerializeHost
from config import SESSIONS_EXPIRY, HASH_NAME_EXPIRY

from typing import Any
from redis import Redis
import secrets
import hashlib

class RedisAdapter(RedisHost):
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, redis_url: str = 'redis://127.0.0.1:6379/1'):
        if not type(self)._initialized:
            self.redis_client = Redis.from_url(redis_url)
            type(self)._initialized = True

    def hget(self, hash_name: str, key: str):
        return self.redis_client.hget(hash_name, key)

    def hset(self, hash_name: str, key: str, value, expire: int | None = None):
        self.redis_client.hset(hash_name, key, value)

        if expire: self.expire(hash_name, expire)
        else: self.expire(hash_name, HASH_NAME_EXPIRY)

    def hdel(self, hash_name: str, key: str):
        self.redis_client.hdel(hash_name, key)

    def expire(self, hash_name: str, expire: int):
        self.redis_client.expire(hash_name, expire, nx=True)


class RedisSessionAdapter(RedisSessionHost):
    def __init__(self, redis_adapter: RedisHost, serialize_adapter: SerializeHost, session_key: str | None = None):
        self.redis_adapter = redis_adapter
        self._serialize_adapter = serialize_adapter
        self._session_key = session_key

    @property
    def session_key(self) -> str:
        if not self._session_key:
            self._session_key = secrets.token_hex(8)
        return self._session_key

    @property
    def serialize_adapter(self) -> SerializeHost:
        if not self._serialize_adapter:
            raise ValueError("")
        return self._serialize_adapter
    
    def hand_over_session_key(self, session_key: str) -> None:
        self._session_key = session_key

    def get(self, key: str, default: Any = None, deserialize: bool = True, *args, **kwargs) -> Any:
        session_data = self.redis_adapter.hget(self._get_session_key(), key)
        if not session_data:
            return default

        if deserialize:
            session_data = self.serialize_adapter.deserialize(session_data, *args, **kwargs)
        return session_data

    def pop(self, key: str, default: Any = None, deserialize: bool = True, *args, **kwargs) -> Any:
        session_data = self.redis_adapter.hget(self._get_session_key(), key)
        if session_data:
            self.redis_adapter.hdel(self._get_session_key(), key)
            if deserialize:
                session_data = self.serialize_adapter.deserialize(session_data, *args, **kwargs)
            return session_data
        return default

    def set(self, key: str, data: Any, expire: int = SESSIONS_EXPIRY, serialize: bool = True):
        if serialize:
            data = self.serialize_adapter.serialize(data)
        self.redis_adapter.hset(self._get_session_key(), key, data, expire*60)

    def delete(self, key):
        self.redis_adapter.hdel(self._get_session_key(), key)

    def _get_session_key(self):
        if not self.session_key:
            raise ValueError("Session key is not initialized. Ensure the session is created.")
        return f"electro:user:session:{self.session_key}"
    
    def cache_key(self, key: str, prefix: str = "cache") -> str:
        """Generate a cache key."""
        key = hashlib.md5(key.encode("utf-8")).hexdigest()
        return f"{prefix}_{key}"
