from core.utils.exceptions import InvalidDependencyException
from .base_dto import DTO
from ..domain.interfaces.hosts.redis import RedisSessionHost

from typing import Callable
from functools import wraps
import inspect

class BaseCachingMixin:
    session_adapter: RedisSessionHost

    def __init__(self, session_adapter: RedisSessionHost | type[RedisSessionHost]):
        BaseCachingMixin.set_session_adapter(self._resolve_dependency(session_adapter))

    def _resolve_dependency(self, dependency) -> RedisSessionHost:
        """Helper method to instantiate class if type is passed"""
        if not isinstance(dependency, RedisSessionHost) and not issubclass(dependency, RedisSessionHost):
            raise InvalidDependencyException(f"{dependency} isn't a {RedisSessionHost.__name__} nor it's instance")
        return dependency() if isinstance(dependency, type) else dependency

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
                
                cached_data = cls.session_adapter.get(cache_key, dtos=dtos) if dtos else cls.session_adapter.get(cache_key)
                if not cached_data:
                    cached_data = func(instance, *args, **kwargs) #actually raw data
                    cls.session_adapter.set(cache_key, cached_data)
                return cached_data
            return wrapper
        return decorator
