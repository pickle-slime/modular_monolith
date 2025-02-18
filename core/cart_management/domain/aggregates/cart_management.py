from ....utils.domain.value_objects.common import ForeignUUID
from ....utils.domain.entity import Entity
from ..entities.cart_management import CartItem, WishlistItem

from dataclasses import dataclass, field
import uuid

@dataclass(kw_only=True)
class Cart(Entity):
    total_price: int = field(default=0)
    quantity: int = field(default=0)

    user: ForeignUUID | uuid.UUID = field(default=None)

    items: list[CartItem] = field(default_factory=list)

@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: int = field(default=0)
    quantity: int = field(default=0)

    user: ForeignUUID | uuid.UUID = field(default=None)

    items: list[WishlistItem] = field(default_factory=list)
