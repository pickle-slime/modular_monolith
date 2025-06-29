from core.utils.domain.interfaces.hosts.base_host import BaseHost
from core.utils.application.base_dto import DTO

from abc import abstractmethod
from typing import Any

class SerializeHost(BaseHost):
    @abstractmethod
    def serialize(self, raw_data) -> str:
        pass

    @abstractmethod
    def deserialize(self, serialized_data: str, dtos: list[type[DTO]] | None = None) -> Any:
        pass
