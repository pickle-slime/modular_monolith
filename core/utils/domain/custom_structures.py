from core.shop_management.domain.entities.shop_management import ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity

from django.db.models.manager import Manager

from typing import Optional, Union, Iterable, Generic, TypeVar

MIN_SIZES = 0
MAX_SIZES = 5
MIN_IMAGES = 0
MAX_IMAGES = 10

T = TypeVar('T')

class ProductEntityListBase(Iterable[T], Generic[T]):
    def __init__(self, entities: Iterable):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]


class ProductSizesEntityList(ProductEntityListBase):
    def __init__(self, entities: Iterable[ProductSizeEntity]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_SIZES, max_length=MAX_SIZES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__}  contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__}  contains more than {max_length} entities.")

class ProductImagesEntityList(ProductEntityListBase):
    def __init__(self, entities: Iterable[ProductImageEntity]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_IMAGES, max_length=MAX_IMAGES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__} contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__} contains more than {max_length} entities.")


def has_select_related(queryset: Manager, field_name: str) -> Union[str, False]:
        '''This function should be out of the domain layer'''
        related_fields = getattr(queryset.query, '_select_related', None)
        if related_fields is None:
            return False
        return field_name in related_fields