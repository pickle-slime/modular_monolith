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
    name: CommonNameField | None = field(default=None)
    slug: CommonSlugField | None = field(default=None)
    description: str | None = field(default=None)
    details: str | None = field(default=None)
    image: ImageField | None = field(default=None)
    price: float | None = field(default=None)
    discount: PercentageField | None = field(default=None)
    color: str | None = field(default=None)
    in_stock: int | None = field(default=None)
    count_of_selled: int | None = field(default=None)
    time_created: datetime | None = field(default=None)
    time_updated: datetime | None = field(default=None)

    brand: ForeignUUID | uuid.UUID | None = field(default=None)
    category: ForeignUUID | uuid.UUID | None = field(default=None)
    seller: uuid.UUID | None = field(default=None)

    sizes: ProductSizesEntityList[ProductSize] | None = field(default=None)
    images: ProductImagesEntityList[ProductImage] | None = field(default=None)
