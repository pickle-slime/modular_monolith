from core.utils.domain.entity import Entity
from ..value_objects.cart_management import CartItem as CartItemVO, Size as SizeVO

from decimal import Decimal
from dataclasses import dataclass, field
import uuid
    
@dataclass(kw_only=True)
class Cart(Entity):
    total_price: Decimal = field(default=None)
    quantity: int = field(default=None)

    user: uuid.UUID = field(default=None)

    items: dict[CartItemVO] = field(default=None)

@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str = field(default=None)
    qty: int = field(default=None)
    image: str = field(default=None)
    price: Decimal = field(default=None)

    size: SizeVO = field(default=None)