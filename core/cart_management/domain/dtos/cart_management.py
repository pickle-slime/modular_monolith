from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class AddToWishlistDomainDTO:
    color: str | None
    qty: int | None
    size: uuid.UUID | None 

@dataclass(frozen=True)
class AddToCartDomainDTO:
    color: str
    qty: int
    size: uuid.UUID

