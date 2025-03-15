from .base_dto import DTO
from ..domain.interfaces.hosts.redis import RedisSessionHost
from ..infrastructure.serializers.json_decoder import PydanticJSONDecoder
from ..infrastructure.serializers.json_encoder import PydanticJSONEncoder

from typing import Any, Callable
from functools import wraps
import hashlib
import inspect
import json

class BaseCachingMixin:
    session_adapter: RedisSessionHost

    def __init__(self, session_adapter: RedisSessionHost):
        BaseCachingMixin.set_session_adapter(session_adapter)

    @classmethod
    def set_session_adapter(cls, session_adapter: RedisSessionHost):
        cls.session_adapter = session_adapter

    @classmethod
    def cache_result(cls, key_template: str, prefix: str = "{self.__class__.__name__}.{func.__name__}", dtos: list[type[DTO]] | None = None) -> Callable:
        """
        Retrieve data from cache or compute it if not cached.

        :key_template - is the dynamic part of the cached key. The key itself is built with key_template and names of class and func of the wrapped method.
        :prefix - is non-encoded part of the cache key
        :dtos - expects pydantic data transfer objects that will be serialized into json
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(instance, *args, **kwargs):
                # Get the function signature and bind the arguments
                sig = inspect.signature(func)
                bound_args = sig.bind(instance, *args, **kwargs)
                bound_args.apply_defaults()

                # combine args and kwargs and exclude 'self' from the arguments
                bound_arguments = {k: v for k, v in bound_args.arguments.items() if k != 'self'}

                _key = f"{instance.__class__.__name__}.{func.__name__}." + key_template.format(self=instance, func=func, **bound_arguments)
                _prefix = prefix.format(self=instance, func=func, **bound_arguments)
                cache_key = cls.session_adapter.cache_key(_key, _prefix)
                
                cached_data = cls.session_adapter.get(cache_key)
                if not cached_data:
                    cached_data = json.dumps(func(instance, *args, **kwargs), cls=PydanticJSONEncoder)
                    cls.session_adapter.set(cache_key, cached_data)
                return json.loads(cached_data, object_hook=PydanticJSONDecoder.from_dict(dtos))
            return wrapper
        return decorator