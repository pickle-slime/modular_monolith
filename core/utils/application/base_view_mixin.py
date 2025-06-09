from core.utils.domain.interfaces.i_repositories.base_repository import Repository
from core.utils.domain.interfaces.hosts.base_host import BaseHost, Host
from .base_factories import BaseServiceFactory
from .base_service import Service, BaseService

from typing import Any, Union, Generic

TRepository = Union[Repository | type[Repository]]
THost = Union[Host | type[Host]]
TService = Union[Service | type[Service]]

class BaseViewMixin(Generic[Service, Repository]):
    service_class: type[BaseService] | None = None

    repository_classes: dict[str, TRepository] = {}
    adapter_classes: dict[str, THost] = {}
    service_classes: dict[str, TService] = {}

    service_args: dict[str, dict[str, Any]] = {}
    adapter_args: dict[str, dict[str, Any]] = {}
    repository_args: dict[str, dict[str, Any]] = {}

    service_factory: BaseServiceFactory | None = None
    service_factory_method_name: str | None = None

    @property
    def service(self) -> Service:
        if not hasattr(self, "_service_instance"):
            if self.service_factory: 
                self._service_instance = self.update_factory()
            elif self.service_class:
                services = self.update_services() or {}
                repositories = self.update_repositories() or {}
                adapters = self.update_adapters() or {}
                self._service_instance = self.service_class(**services, **repositories, **adapters)
            else: TypeError(f"{self.__class__.__name__}: The service class is neither defined nor implemented with repository classes or a service factory.")

        return self._service_instance

    def update_services(self) -> dict[str, Service] | None:
        if not hasattr(self, "_service_instances"):
            self._service_instances = {}
            for name, repo_class in self.service_classes.items():
                try:
                    self._service_instances[name] = repo_class(**self.service_args[name]) if name in self.service_args else repo_class()
                except TypeError:
                    self._service_instances[name] = repo_class

            return self._service_instances

    def update_repositories(self) -> dict[str, Repository] | None:  
        if not hasattr(self, "_repository_instances"):
            self._repository_instances = {}
            for name, repo_class in self.repository_classes.items():
                try:
                    self._repository_instances[name] = repo_class(**self.repository_args[name]) if name in self.repository_args else repo_class()
                except TypeError:
                    self._repository_instances[name] = repo_class

            return self._repository_instances
        
    def update_adapters(self) -> dict[str, BaseHost] | None:    
        if not hasattr(self, "_adapter_instances"):
            self._adapter_instances = {}
            for name, repo_class in self.adapter_classes.items():
                try:
                    self._adapter_instances[name] = repo_class(**self.adapter_args[name]) if name in self.adapter_args else repo_class()
                except TypeError:
                    self._adapter_instances[name] = repo_class

            return self._adapter_instances
    
    def update_factory(self) -> type[BaseService]:
        if self.service_class is None:
            raise ValueError(f"{self.__class__.__name__}: View should define his own service")
        
        if not self.service_factory:
            raise ValueError(f"{self.__class__.__name__}: Service factory is not defined.")

        if self.repository_classes and hasattr(self.service_factory, "_repositories"):
            self.service_factory._repositories |= self.repository_classes
        if self.adapter_classes and hasattr(self.service_factory, "_adapters"):
            self.service_factory._adapters |= self.adapter_classes
        if self.service_classes and hasattr(self.service_factory, "_services"):
            self.service_factory._services |= self.service_classes

        if self.service_factory_method_name:
            service_method = getattr(self.service_factory, self.service_factory_method_name, None)
            if service_method:
                self._service_instance = service_method()
            else:
                raise AttributeError(
                    f"{self.__class__.__name__}: Factory does not have a method '{self.service_factory_method_name}'."
                )
        else:
            self._service_instance = self.service_factory.create_service(self.service_class, self.adapter_args, self.repository_args, self.service_args)

        return self._service_instance
    
        
    def setup_dynamic_dependencies(self, instance_name: str, dependencies: dict[str, Any]) -> None:
        for key, dependency in dependencies.items():
            if instance_name in self.repository_args:
                if key in self.repository_args[instance_name]:
                    self.repository_args[instance_name][key] = dependency
                else:
                    raise ValueError(f"{self.__class__.__name__}: '{key}' not found in repository_args['{instance_name}']")
            elif instance_name in self.adapter_args:
                if key in self.adapter_args[instance_name]:
                    self.adapter_args[instance_name][key] = dependency
                else:
                    raise ValueError(f"{self.__class__.__name__}: '{key}' not found in adapter_args['{instance_name}']")
            elif instance_name in self.service_args:
                if key in self.service_args[instance_name]:
                    self.service_args[instance_name][key] = dependency
                else:
                    raise ValueError(f"{self.__class__.__name__}: '{key}' not found in service_args['{instance_name}']")
            else:
                raise ValueError(f"{self.__class__.__name__}: There is no {instance_name} in repository_args, adapter_args, and service_args")
