from core.utils.domain.entity import Entity
from ..value_objects.cart_management import CartItem, Size

from dataclasses import dataclass, field
import uuid
    
@dataclass(kw_only=True)
class Cart(Entity):
    total_price: int = field(default=0)
    quantity: int = field(default=0)

    user: uuid.UUID = field(default=None)

    items: list[CartItem] = field(default_factory=list)

@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str = field(default=None)
    qty: int = field(default=None)

    size: uuid.UUID = field(default=None)
    size_snapshot: Size = field(default_factory=Size)

    def to_snapshot(self, size_details):
        """
        Capture a snapshot of size details at the time of wishlist addition.
        """
        self.size_snapshot = {
            "length": size_details.length,
            "width": size_details.width,
            "height": size_details.height,
            "weight": size_details.weight,
        }