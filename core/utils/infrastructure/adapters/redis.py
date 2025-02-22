from core.utils.domain.interfaces.hosts.redis import RedisHost, RedisSessionHost
from config import SESSIONS_EXPIRY, HASH_NAME_EXPIRY

from typing import Any
from redis import Redis
import secrets
import json
import pickle

class RedisAdapter(RedisHost):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, redis_url: str = 'redis://127.0.0.1:6379/1'):
        if not type(self)._initialized:
            self.redis_client = Redis.from_url(redis_url)
            type(self)._initialized = True

    def hget(self, hash_name: str, key: str):
        return self.redis_client.hget(hash_name, key)

    def hset(self, hash_name: str, key: str, value, expire: int = None):
        self.redis_client.hset(hash_name, key, value)

        if expire: self.expire(hash_name, expire)
        else: self.expire(hash_name, HASH_NAME_EXPIRY)

    def hdel(self, hash_name: str, key: str):
        self.redis_client.hdel(hash_name, key)

    def expire(self, hash_name: str, expire: int):
        self.redis_client.expire(hash_name, expire, nx=True)


class RedisSessionAdapter(RedisSessionHost):
    def __init__(self, redis_adapter: RedisAdapter, session_key: str = None):
        self.redis_adapter = redis_adapter
        self._session_key = session_key

    @property
    def session_key(self) -> None:
        if not self._session_key:
            self._session_key = secrets.token_hex(8)
        return self._session_key
    
    def hand_over_session_key(self, session_key: str) -> None:
        self._session_key = session_key

    def _deserialize_data(self, session_data):
        """Helper method to deserialize JSON or Pickle data."""
        try:
            return json.loads(session_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            try:
                return pickle.loads(session_data)
            except Exception:
                return None

    def get(self, key: str, default: Any = None) -> Any:
        session_data = self.redis_adapter.hget(self._get_session_key(), key)
        if session_data:
            return self._deserialize_data(session_data)
            # if isinstance(data, dict):
            #     return data.get(key, default)
        return default

    def pop(self, key: str, default: Any = None) -> Any:
        session_data = self.redis_adapter.hget(self._get_session_key(), key)
        if session_data:
            data = self._deserialize_data(session_data)
            self.redis_adapter.hdel(self._get_session_key(), key)
            return data
            # if isinstance(data, dict):
            #     value = data.pop(key, default)
            #     self.redis_adapter.hset(
            #         self._get_session_key(),
            #         key,
            #         pickle.dumps(data),
            #         expire=SESSIONS_EXPIRY,
            #     )
            #     return value
        return default

    def set(self, key: str, value: Any, expire: int = SESSIONS_EXPIRY):
        if isinstance(value, dict):
            value = json.dumps(value)
        else:
            value = pickle.dumps(value)
        self.redis_adapter.hset(self._get_session_key(), key, value, expire*60)

    def delete(self, key):
        self.redis_adapter.hdel(self._get_session_key(), key)

    def _get_session_key(self):
        if not self.session_key:
            raise ValueError("Session key is not initialized. Ensure the session is created.")
        return f"electro:user:session:{self.session_key}"
