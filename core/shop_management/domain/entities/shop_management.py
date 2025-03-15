from core.utils.domain.entity import *
from ..value_objects.shop_management import *
from ....utils.domain.value_objects.common import *

from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class Category(Entity):
    name: CommonNameField | str = field(default=None)
    slug: CommonSlugField | str = field(default=None)
    count_of_deals: int = field(default=None)

    def __post_init__(self):
        if isinstance(self.name, str):
            self.name = CommonNameField(self.name)

        if isinstance(self.slug, str):
            self.slug = CommonSlugField(self.slug)
            

@dataclass(kw_only=True)
class Brand(Entity):
    name: CommonNameField = field(default=None)
    slug: CommonSlugField = field(default=None)
    count_of_deals: int = field(default=None)


@dataclass(kw_only=True)
class ProductSize(Entity):
    size: str = field(default=None)
    length: Decimal = field(default=None)
    width: Decimal = field(default=None)
    height: Decimal = field(default=None)
    weight: Decimal = field(default=None)

    product: ForeignUUID | uuid.UUID = field(default=None)

@dataclass(kw_only=True)
class ProductImage(Entity):
    image: ImageField = field(default=None)

    product: ForeignUUID | uuid.UUID = field(default=None)
