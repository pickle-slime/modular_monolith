from core.utils.domain.entity import Entity
from ..entities.cart_management import CartItem, WishlistItem

from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: int = field(default=0)
    quantity: int = field(default=0)

    user: uuid.UUID = field(default=None)

    items: list[WishlistItem] = field(default_factory=list)
