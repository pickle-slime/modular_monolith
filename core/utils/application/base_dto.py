from ..domain.entity import EntityType

from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

class BaseDTO(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_entity(cls: type['DTO'], entity: EntityType) -> 'DTO':
        pass

DTO = TypeVar("DTO", bound=BaseDTO)