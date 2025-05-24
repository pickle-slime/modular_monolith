from ..domain.entity import EntityType

from abc import abstractmethod
from typing import TypeVar, Protocol, Any

DTO = TypeVar("DTO", covariant=True)

class BaseDTO(Protocol[DTO]):
    '''
    The BaseDTO represents DTOs with bloated responsibilities. All DTOs inherited from the BaseDTO 
    are supposed to align with a BaseDTO convention: DTO might be used as a Python object, a JSON object, or
    a Python object in the render engine context. As a Python object, the DTO has default values settled as None for all
    fields to represent empty fields (which means an aggregate or an entity doesn't have all or some fields in a concrete case).
    As a JSON object, the DTO excludes all None fields. And as a Python object in the render context, the DTO must populate
    all None fields with empty values depending on field annotation.
    '''

    def _get_default(self, annotation: type) -> Any:
        """Returns the appropriate strategy instance, favoring custom strategies if available."""
        ...
    
    def _resolve_annotation(self, annotation: type[Any] | None) -> type:
        ...
    
    def populate_none_fields(self) -> DTO:
        '''
        Populates all None fields in the DTO to hand it over to a render engine.
        The DTOs should use a built-in model_dump or model_dump_json with exclude_none=True.
        '''
        ...

    def model_dump(self, *args, **kwargs):
        """Overrides Pydantic's default dump method to exclude None values."""
        ...

class BaseEntityDTO(BaseDTO[DTO], Protocol[DTO]):
    @classmethod
    @abstractmethod
    def from_entity(cls: type["BaseEntityDTO"], entity: EntityType) -> DTO:
        pass
