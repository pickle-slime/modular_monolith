from core.utils.domain.entity import Entity
from ..value_objects.cart_management import CartItem as CartItemVO, Size as SizeVO

from decimal import Decimal
from typing import Any
from dataclasses import dataclass, field
import uuid
  
@dataclass(kw_only=True)
class Cart(Entity):
    total_price: Decimal | None = field(default=None)
    quantity: int | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    items: dict[uuid.UUID, CartItemVO] | None = field(default=None)
 
@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str | None = field(default=None)
    qty: int | None = field(default=None)
    image: str | None = field(default=None)
    price: Decimal | None = field(default=None)

    size: SizeVO | None = field(default=None)
    
    _size_cls: type[SizeVO] = SizeVO

    @classmethod
    def map_raw_data(cls, raw_data: dict[str, Any]) -> "WishlistItem":
        price = raw_data.get("price", None)
        if price is None:
            raise ValueError(f"{cls.__name__}.{cls.map_raw_data.__name__} didn't get price value")

        size = raw_data.get("size", None)
        if not isinstance(size, dict) and not isinstance(size, SizeVO):
            raise ValueError(f"{cls.__name__}.{cls.map_raw_data.__name__} didn't get size data")

        return cls(
                color=raw_data.get("color", "Black"),
                qty=raw_data.get("qty", 1),
                image=raw_data.get("image", "/"),
                price=price,
                size=size if isinstance(size, SizeVO) else cls._size_cls.map_raw_data(size)
            )
