from dataclasses import dataclass
from decimal import Decimal
import uuid

@dataclass(frozen=True)
class AddToWishlistDomainDTO:
    price: Decimal | None
    color: str | None
    qty: int | None
    image: str | None 
    size: uuid.UUID | None 

