from core.cart_management.domain.entity import Entity
from core.cart_management.domain.exceptions import ValidationError
from ..dtos.cart_management import AddToWishlistDomainDTO, AddToCartDomainDTO

from typing import Any
from dataclasses import dataclass, field
import uuid

@dataclass(kw_only=True)
class CartItem(Entity):
    color: str = field(default="Black")
    qty: int = field(default=0)
    size: uuid.UUID

    @classmethod
    def map_raw_data(cls, raw_data: dict[str, Any]) -> "CartItem":
        size = raw_data.get("size")
        if not isinstance(size, uuid.UUID):
            raise ValidationError("Missing size")
        return cls._build(
                color=raw_data.get("color", "Black"),
                qty=raw_data.get("qty", 0),
                size=size,
            )
    
    @classmethod
    def map_domain_dto(cls, domain_dto: AddToCartDomainDTO) -> "CartItem":
        return cls._build(
                color=domain_dto.color,
                qty=domain_dto.qty,
                size=domain_dto.size
            )

    @classmethod
    def _build(
                cls,
                color: str, 
                qty: int ,
                size: uuid.UUID
            ) -> "CartItem":
        return cls(
                color=color or "Black",
                qty=qty or 1,
                size=size,
            )
   
 
@dataclass(kw_only=True)
class WishlistItem(Entity):
    color: str | None = field(default=None)
    qty: int | None = field(default=None)

    size: uuid.UUID | None = field(default=None)

    @classmethod
    def map_raw_data(cls, raw_data: dict[str, Any]) -> "WishlistItem":
        return cls._build(
                color=raw_data.get("color", None),
                qty=raw_data.get("qty", None),
                size=raw_data.get("size", None)
            )
    
    @classmethod
    def map_domain_dto(cls, domain_dto: AddToWishlistDomainDTO) -> "WishlistItem":
        return cls._build(
                color=domain_dto.color,
                qty=domain_dto.qty,
                size=domain_dto.size
            )

    @classmethod
    def _build(
                cls,
                color: str | None, 
                qty: int | None,
                size: uuid.UUID | None
            ) -> "WishlistItem":
        return cls(
                color=color or "Black",
                qty=qty or 1,
                size=size or None,
            )
