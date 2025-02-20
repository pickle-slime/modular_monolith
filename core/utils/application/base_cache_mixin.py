from django.core.cache import cache
from django.utils.encoding import force_bytes

from ..domain.entity import EntityType
from .base_dto import DTO
from ..domain.value_objects.common import BaseEntityCollection

from pydantic import BaseModel
from typing import Any, Callable
from functools import wraps
from datetime import datetime
import hashlib
import inspect
import json
import uuid

class PydanticJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            # Recursively encode DTOs while preserving structure
            return {key: self.default(value) for key, value in obj.model_dump().items()} | {"__class__": obj.__class__.__name__}
        if isinstance(obj, list):
            return [self.default(item) for item in obj] 
        if isinstance(obj, dict):
            return {key: self.default(value) for key, value in obj.items()}
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        if isinstance(obj, str) or isinstance(obj, int) or obj == None:
            return obj
        
        return super().default(obj)

class PydanticJSONDecoder:
    @staticmethod
    def from_dict(dtos: list[type[DTO]]):
        def decode(d):
            if isinstance(d, dict):
                if "__class__" in d:
                    for dto in dtos:
                        if d["__class__"] == dto.__name__:
                            dto_data = {k: decode(v) for k, v in d.items() if k != "__class__"}
                            return dto(**dto_data)
                return {k: decode(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [decode(item) for item in d]
            return d

        return decode

class BaseCachingMixin:
    cache_timeout = 60 * 15  

    @staticmethod
    def _cache_key(key: str, prefix: str = "cache") -> str:
        """Generate a cache key."""
        key = hashlib.md5(force_bytes(key, strings_only=True)).hexdigest()
        return f"{prefix}_{key}"

    @staticmethod
    def cache_result(key_template: str, prefix: str = "{self.__class__.__name__}.{func.__name__}", dtos: list[type[DTO]] | None = None) -> Callable:
        """
        Retrieve data from cache or compute it if not cached.

        :key_template - is the dynamic part of the cached key. The key itself is built with key_template and names of class and func of the wrapped method.
        :prefix - is non-encoded part of the cache key
        :dtos - expects pydantic data transfer objects that will be serialized into json
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Get the function signature and bind the arguments
                sig = inspect.signature(func)
                bound_args = sig.bind(self, *args, **kwargs)
                bound_args.apply_defaults()

                # combine args and kwargs and exclude 'self' from the arguments
                bound_arguments = {k: v for k, v in bound_args.arguments.items() if k != 'self'}

                _key = f"{self.__class__.__name__}.{func.__name__}." + key_template.format(self=self, func=func, **bound_arguments)
                _prefix = prefix.format(self=self, func=func, **bound_arguments)
                cache_key = BaseCachingMixin._cache_key(_key, _prefix)
                
                cached_data = cache.get(cache_key)
                if not cached_data:
                    cached_data = json.dumps(func(self, *args, **kwargs), cls=PydanticJSONEncoder)
                    cache.set(cache_key, cached_data, BaseCachingMixin.cache_timeout)
                return json.loads(cached_data, object_hook=PydanticJSONDecoder.from_dict(dtos))
            return wrapper
        return decorator
    
    def get_cached_entities(self, key: str, entities: BaseEntityCollection[EntityType] | list[EntityType], prefix: str = "entities") -> BaseEntityCollection | Any:
        cache_key = self._cache_key(key, prefix=prefix)
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = BaseEntityCollection(entities)
            cache.set(key=cache_key, value=cached_data, timeout=self.cache_timeout)
        return cached_data