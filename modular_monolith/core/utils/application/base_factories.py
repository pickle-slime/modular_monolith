from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository, Repository
from core.utils.domain.interfaces.hosts.base_host import BaseHost, Host
from core.utils.application.base_service import Service 

from typing import Union
import inspect

TRepository = Union[type[Repository] | Repository | None]
THost = Union[type[Host] | Host | None]
TService = Union[type[Service] | Service | None]

class BaseServiceFactory:
    def __init__(
            self, 
            repositories: dict[str, TRepository] = dict(), 
            adapters: dict[str, THost] = dict(), 
            services: dict[str, TService] = dict(),
        ):
        
        self._services = services
        self._repositories = repositories
        self._adapters = adapters

    def create_service(self, service_class: type[Service], adapter_args: dict = {}, repository_args: dict = {}, service_args: dict = {}) -> Service:
        kwargs = {}

        for cls in inspect.getmro(service_class):
            if cls == object:
                break

            signature = inspect.signature(cls.__init__)
            for name, param in signature.parameters.items():
                if name == 'self':
                    continue

                if name in self._repositories and name not in kwargs:
                    init_args = repository_args.get(name, None)
                    value = self._repositories[name]
                    kwargs[name] = value(**init_args) if callable(value) and init_args else value() if callable(value) else value
                elif name in self._adapters and name not in kwargs:
                    init_args = adapter_args.get(name, None)
                    value = self._adapters[name]
                    kwargs[name] = value(**init_args) if callable(value) and init_args else value() if callable(value) else value
                elif name in self._services and name not in kwargs:
                    init_args = service_args.get(name, None)
                    value = self._services[name]
                    kwargs[name] = value(**init_args) if callable(value) and init_args else value() if callable(value) else value
                elif param.default is not inspect.Parameter.empty and name not in kwargs:
                    kwargs[name] = param.default

        return service_class(**kwargs)
    

class LazyDependencyInjector:
    """
        This is so-called injector handles service dependencies like repositories, adapters, and other services
        within the context of the RESTful approach. To put it simply, the injector is supposed to pass on dependencies
        instead of initialization, so we would have an opportunity to use lazy-loading within services.
    """
    def __init__(self, repositories: dict[str, type[BaseRepository]] = {}, adapters: dict[str, type[BaseHost]] = {}, services: dict[str, type[Service]] = {}):
        self._services = services
        self._repositories = repositories
        self._adapters = adapters

    def load_service(self, service_class: type[Service]) -> Service:
        kwargs = {}

        for cls in inspect.getmro(service_class):
            if cls == object:
                break

            signature = inspect.signature(cls.__init__)
            for name, param in signature.parameters.items():
                if name == 'self':
                    continue

                if name in self._repositories and name not in kwargs:
                    kwargs[name] = self._repositories[name]
                elif name in self._adapters and name not in kwargs:
                    kwargs[name] = self._adapters[name]
                elif name in self._services and name not in kwargs:
                    kwargs[name] = self._services[name]
                elif param.default is not inspect.Parameter.empty and name not in kwargs:
                    kwargs[name] = param.default

        return service_class(**kwargs)
