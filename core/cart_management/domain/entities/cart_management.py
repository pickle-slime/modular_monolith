from core.utils.domain.entity import Entity
from ..value_objects.cart_management import CartItem as CartItemVO

from decimal import Decimal
from dataclasses import dataclass, field
import uuid
  
@dataclass(kw_only=True)
class Cart(Entity):
    total_price: Decimal | None = field(default=None)
    quantity: int | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    items: dict[uuid.UUID, CartItemVO] | None = field(default=None)
 
@dataclass(kw_only=True)
class Size(Entity):
    length: Decimal | None = field(default=None)
    width: Decimal | None = field(default=None)
    height: Decimal | None = field(default=None)
    weight: Decimal | None = field(default=None)
 
@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str | None = field(default=None)
    qty: int | None = field(default=None)
    image: str | None = field(default=None)
    price: Decimal | None = field(default=None)

    size: Size | None = field(default=None)

    def __post_init__(self):
        if self.color is None: self.color = "Black"
        if self.qty is None: self.qty = 0
        if self.image is None: self.image = "/"
        if self.price is None: self.price = Decimal(0)
