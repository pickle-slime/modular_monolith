from ....utils.domain.entity import Entity
from ....utils.domain.value_objects.common import ForeignUUID

from dataclasses import dataclass, field
from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class CartItem(Entity):
    color: str = field(default=None)
    qty: int = field(default=None)

    size: uuid.UUID = field(default=None)
    size_snapshot: dict = field(default=None)

    def to_snapshot(self, size_details):
        """
        Capture a snapshot of size details at the time of cart addition.
        """
        self.size_snapshot = {
            "length": size_details.length,
            "width": size_details.width,
            "height": size_details.height,
            "weight": size_details.weight,
        }

@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str = field(default=None)
    qty: int = field(default=None)

    size: uuid.UUID = field(default=None)
    size_snapshot: dict[
        'length': Decimal,
        'width': Decimal,
        'height': Decimal,
        'weight': Decimal,
    ] = field(default=None) 

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