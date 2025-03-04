from core.utils.domain.entity import *
from ..value_objects.shop_management import *
from ....utils.domain.value_objects.common import *

from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class Category(Entity):
    name: CommonNameField | str
    slug: CommonSlugField | str
    count_of_deals: int = 0

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = CommonNameField(self.name)

        if isinstance(self.slug, str):
            self.slug = CommonSlugField(self.slug)
            

@dataclass(kw_only=True)
class Brand(Entity):
    name: CommonNameField
    slug: CommonSlugField
    count_of_deals: int = 0


@dataclass(kw_only=True)
class ProductSize(Entity):
    size: str
    length: Decimal
    width: Decimal
    height: Decimal
    weight: Decimal

    product: ForeignUUID | uuid.UUID

@dataclass(kw_only=True)
class ProductImage(Entity):
    image: ImageField

    product: ForeignUUID | uuid.UUID
