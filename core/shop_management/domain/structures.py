from typing import Optional, Iterable

from core.shop_management.domain.entities.shop_management import ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity

from core.utils.domain.structures import BaseEntityList


MIN_SIZES = 0
MAX_SIZES = 5
MIN_IMAGES = 0
MAX_IMAGES = 10


class ProductSizesEntityList(BaseEntityList):
    def __init__(self, entities: Iterable[ProductSizeEntity]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_SIZES, max_length=MAX_SIZES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__}  contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__}  contains more than {max_length} entities.")

class ProductImagesEntityList(BaseEntityList):
    def __init__(self, entities: Iterable[ProductImageEntity]):
        super().__init__(entities)
        self.validate_length(min_length=MIN_IMAGES, max_length=MAX_IMAGES)

    def validate_length(self, min_length: int, max_length: Optional[int] = None) -> None:
        if len(self._entities) < min_length:
            raise ValueError(f"{self.__class__.__name__} contains fewer than {min_length} entities.")
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__} contains more than {max_length} entities.")