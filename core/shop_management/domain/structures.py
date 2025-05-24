from typing import Optional, Iterable, Generic

from core.shop_management.domain.entities.shop_management import ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity, ProductSizeType, ProductImageType

from core.shop_management.domain.entity import EntityType

MIN_SIZES = 0
MAX_SIZES = 5
MIN_IMAGES = 0
MAX_IMAGES = 10

class BaseEntityList(Generic[EntityType]):
    def __init__(self, entities: Iterable[EntityType]):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]

class ProductSizesEntityList(Generic[ProductSizeType], BaseEntityList[ProductSizeEntity]):
    def __init__(self, entities: Iterable[ProductSizeType]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_SIZES, max_length=MAX_SIZES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__}  contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__}  contains more than {max_length} entities.")

class ProductImagesEntityList(Generic[ProductImageType], BaseEntityList[ProductImageEntity]):
    def __init__(self, entities: Iterable[ProductImageType]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_IMAGES, max_length=MAX_IMAGES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__} contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__} contains more than {max_length} entities.")
