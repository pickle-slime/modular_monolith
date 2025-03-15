from ....utils.domain.value_objects.common import CommonNameField, CommonSlugField, ForeignUUID
from ..structures import ProductSizesEntityList, ProductImagesEntityList
from ..value_objects.shop_management import ImageField, PercentageField
from ..entities.shop_management import ProductSize, ProductImage
from ....utils.domain.entity import Entity

from datetime import datetime
from dataclasses import dataclass, field
import uuid

@dataclass(kw_only=True)
class Product(Entity):
    name: CommonNameField = field(default=None)
    slug: CommonSlugField = field(default=None)
    description: str = field(default=None)
    details: str = field(default=None)
    image: ImageField = field(default=None)
    price: float = field(default=None)
    discount: PercentageField = field(default=None)
    color: str = field(default=None)
    in_stock: int = field(default=None)
    count_of_selled: int = field(default=None)
    time_created: datetime = field(default=None)
    time_updated: datetime = field(default=None)

    brand: ForeignUUID | uuid.UUID = field(default=None)
    category: ForeignUUID | uuid.UUID = field(default=None)
    seller: uuid.UUID = field(default=None)

    sizes: ProductSizesEntityList[ProductSize] = field(default=None)
    images: ProductImagesEntityList[ProductImage] = field(default=None)
