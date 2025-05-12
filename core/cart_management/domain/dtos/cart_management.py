from ..value_objects.cart_management import Size as SizeVO

from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class AddToWishlistDomainDTO:
    price: Decimal | None
    color: str | None
    qty: int | None
    image: str | None 
    size: SizeVO | None 

