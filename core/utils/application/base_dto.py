from ..domain.entity import EntityType

from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

DTO = TypeVar("DTO")

class BaseEntityDTO(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_entity(cls: type[DTO], entity: EntityType) -> DTO:
        pass

ENTITY_DTO = TypeVar("DTO", bound=BaseEntityDTO)