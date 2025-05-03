from ..domain.entity import EntityType

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Any, get_origin, get_args
from types import UnionType
from decimal import Decimal
from pydantic import BaseModel, ValidationError
import uuid

DTO = TypeVar("DTO")

class BaseDTO(BaseModel, ABC, Generic[DTO]):
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
        return getattr(self.Config, "_defaults", {}).get(annotation, None)
    
    def _resolve_annotation(self, annotation: type[Any] | None) -> type:
        resolved_annotation: Any = annotation
        while resolved_annotation is not None and get_origin(resolved_annotation) in {Union, UnionType}:
            resolved_annotation = next((t for t in get_args(resolved_annotation) if t is not type(None)), None)
        
        origin = get_origin(resolved_annotation)
        if origin in {list, dict, set, tuple}:
            resolved_annotation = origin

        return resolved_annotation
    
    def populate_none_fields(self) -> "BaseDTO":
        '''
        Populates all None fields in the DTO to hand it over to a render engine.
        The DTOs should use a built-in model_dump or model_dump_json with exclude_none=True.
        '''
        for field_name, field_info in self.model_fields.items():
            field_value = getattr(self, field_name, None)

            if field_value is None and not field_info.is_required():
                default = self._get_default(self._resolve_annotation(field_info.annotation))
                setattr(self, field_name, default)
            
            if isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseDTO):
                try:
                    dto = field_value.populate_none_fields() if isinstance(field_value, BaseDTO) else field_info.annotation().populate_none_fields()
                    setattr(self, field_name, dto)
                except ValidationError:
                    raise ValidationError(f"The DTO field ({field_name}) of the nested DTO ({self.__class__.__name__}) didn't get a value for a mandatory field")

        return self

    def model_dump(self, *args, **kwargs):
        """Overrides Pydantic's default dump method to exclude None values."""
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
    
    class Config:
        json_encoders = {uuid.UUID: str}
        validate_assignment = True 
        populate_by_name=True
        from_attributes = True
        population_by_name = True

        _defaults = {
            str: "",
            int: 0,
            float: 0.0,
            Decimal: Decimal("0"),
            list: [],
            dict: {},
            bool: False,
        }

class BaseEntityDTO(BaseDTO[DTO], Generic[DTO]):
    @classmethod
    @abstractmethod
    def from_entity(cls: type[DTO], entity: EntityType) -> DTO:
        pass

ENTITY_DTO = TypeVar("ENTITY_DTO", bound=BaseEntityDTO)
