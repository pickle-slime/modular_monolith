from ....utils.domain.value_objects.common import CommonNameField, CommonSlugField, ForeignUUID
from ..value_objects.shop_management import ProductSizesCollection, ProductImagesCollection
from ..value_objects.shop_management import ImageField, PercentageField
from ..entities.shop_management import ProductSize, ProductImage
from ....utils.domain.entity import Entity

from datetime import datetime
from dataclasses import dataclass, field
import uuid

@dataclass(kw_only=True)
class Product(Entity):
    name: CommonNameField = field(default=CommonNameField)
    slug: CommonSlugField = field(default=CommonSlugField)
    description: str = field(default=None)
    details: str = field(default=None)
    image: ImageField = field(default=ImageField)
    price: int = field(default=None)
    discount: PercentageField = field(default=PercentageField)
    color: str = field(default=None)
    in_stock: int = field(default=None)
    count_of_selled: int = field(default=None)
    time_created: datetime = field(default=None)
    time_updated: datetime = field(default=None)

    brand: ForeignUUID | uuid.UUID = field(default=None)
    category: ForeignUUID | uuid.UUID = field(default=None)
    seller: ForeignUUID | uuid.UUID = field(default=None)

    sizes: ProductSizesCollection[ProductSize] = field(default=ProductSizesCollection)
    images: ProductImagesCollection[ProductImage] = field(default=ProductImagesCollection)
