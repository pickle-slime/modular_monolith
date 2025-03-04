from django.core.cache import cache
from django.utils.encoding import force_bytes

from ..domain.entity import EntityType
from .base_dto import DTO
from ..domain.value_objects.common import BaseEntityCollection
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

# class BaseCachingMixin:
#     cache_timeout = 60 * 15  

#     def __init__(self, session_adapter: RedisSessionHost):
#         self.session_adapter = session_adapter

#     @staticmethod
#     def _cache_key(key: str, prefix: str = "cache") -> str:
#         """Generate a cache key."""
#         key = hashlib.md5(force_bytes(key, strings_only=True)).hexdigest()
#         return f"{prefix}_{key}"

#     @staticmethod
#     def cache_result(key_template: str, prefix: str = "{self.__class__.__name__}.{func.__name__}", dtos: list[type[DTO]] | None = None) -> Callable:
#         """
#         Retrieve data from cache or compute it if not cached.

#         :key_template - is the dynamic part of the cached key. The key itself is built with key_template and names of class and func of the wrapped method.
#         :prefix - is non-encoded part of the cache key
#         :dtos - expects pydantic data transfer objects that will be serialized into json
#         """
#         def decorator(func: Callable):
#             @wraps(func)
#             def wrapper(self, *args, **kwargs):
#                 # Get the function signature and bind the arguments
#                 sig = inspect.signature(func)
#                 bound_args = sig.bind(self, *args, **kwargs)
#                 bound_args.apply_defaults()

#                 # combine args and kwargs and exclude 'self' from the arguments
#                 bound_arguments = {k: v for k, v in bound_args.arguments.items() if k != 'self'}

#                 _key = f"{self.__class__.__name__}.{func.__name__}." + key_template.format(self=self, func=func, **bound_arguments)
#                 _prefix = prefix.format(self=self, func=func, **bound_arguments)
#                 cache_key = BaseCachingMixin._cache_key(_key, _prefix)
                
#                 cached_data = cache.get(cache_key)
#                 if not cached_data:
#                     cached_data = json.dumps(func(self, *args, **kwargs), cls=PydanticJSONEncoder)
#                     cache.set(cache_key, cached_data, BaseCachingMixin.cache_timeout)
#                 return json.loads(cached_data, object_hook=PydanticJSONDecoder.from_dict(dtos))
#             return wrapper
#         return decorator
    
#     def get_cached_entities(self, key: str, entities: BaseEntityCollection[EntityType] | list[EntityType], prefix: str = "entities") -> BaseEntityCollection | Any:
#         cache_key = self._cache_key(key, prefix=prefix)
#         cached_data = cache.get(cache_key)
#         if not cached_data:
#             cached_data = BaseEntityCollection(entities)
#             cache.set(key=cache_key, value=cached_data, timeout=self.cache_timeout)
#         return cached_data