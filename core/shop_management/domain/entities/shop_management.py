from core.utils.domain.entity import *
from ..value_objects.shop_management import *
from core.utils.domain.value_objects.common import *

from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class Category(Entity):
    name: CommonNameField | str | None = field(default=None)
    slug: CommonSlugField | str | None = field(default=None)
    count_of_deals: int | None = field(default=None)

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = CommonNameField(self.name)

        if isinstance(self.slug, str):
            self.slug = CommonSlugField(self.slug)
            

@dataclass(kw_only=True)
class Brand(Entity):
    name: CommonNameField | None = field(default=None)
    slug: CommonSlugField | None = field(default=None)
    count_of_deals: int | None = field(default=None)


@dataclass(kw_only=True)
class ProductSize(Entity):
    size: str | None = field(default=None)
    length: Decimal | None = field(default=None)
    width: Decimal | None = field(default=None)
    height: Decimal | None = field(default=None)
    weight: Decimal | None = field(default=None)

    product: ForeignUUID | uuid.UUID | None = field(default=None)

ProductSizeType = TypeVar("ProductSizeType", bound=ProductSize)

@dataclass(kw_only=True)
class ProductImage(Entity):
    image: ImageField | None = field(default=None)

    product: ForeignUUID | uuid.UUID | None = field(default=None)

ProductImageType = TypeVar("ProductImageType", bound=ProductImage)


