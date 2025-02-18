from core.utils.domain.interfaces.hosts.redis import RedisHost, RedisSessionHost

from typing import Any
from redis import Redis
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

    def get(self, key: str):
        return self.redis_client.get(key)

    def set(self, key: str, value, expire: int = None):
        self.redis_client.set(key, value, ex=expire)

    def delete(self, key: str):
        self.redis_client.delete(key)


class RedisSessionAdapter(RedisSessionHost):
    def __init__(self, redis_adapter: RedisAdapter, session_key: str):
        self.redis_adapter = redis_adapter
        self.session_key = session_key

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
        session_data = self.redis_adapter.get(self._get_session_key())
        if session_data:
            data = self._deserialize_data(session_data)
            if isinstance(data, dict):
                return data.get(key, default)
        return default

    def pop(self, key: str, default: Any = None) -> Any:
        session_data = self.redis_adapter.get(self._get_session_key())
        if session_data:
            data = self._deserialize_data(session_data)
            if isinstance(data, dict):
                value = data.pop(key, default)
                self.redis_adapter.set(
                    self._get_session_key(),
                    pickle.dumps(data)
                )
                return value
        return default

    def set(self, data: dict, expire: int = None):
        if not isinstance(data, dict):
            raise ValueError("Session data must be a dictionary.")
        self.redis_adapter.set(self._get_session_key(), pickle.dumps(data), expire)

    def delete(self):
        self.redis_adapter.delete(self._get_session_key())

    def _get_session_key(self):
        if not self.session_key:
            raise ValueError("Session key is not initialized. Ensure the session is created.")
        return f":1:django.contrib.sessions.cache{self.session_key}"
