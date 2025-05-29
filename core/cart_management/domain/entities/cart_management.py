from core.cart_management.domain.entity import Entity
from ..dtos.cart_management import AddToWishlistDomainDTO, AddToCartDomainDTO

from typing import Any
from dataclasses import dataclass, field
import uuid

@dataclass(kw_only=True)
class CartItem(Entity):
    color: str | None = field(default=None)
    qty: int | None = field(default=None)
    size: uuid.UUID | None = field(default=None)

    @classmethod
    def map_raw_data(cls, raw_data: dict[str, Any]) -> "CartItem":
        return cls._build(
                color=raw_data.get("color", None),
                qty=raw_data.get("qty", None),
                size=raw_data.get("size", None)
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
                color: str | None, 
                qty: int | None,
                size: uuid.UUID | None
            ) -> "CartItem":
        return cls(
                color=color or "Black",
                qty=qty or 1,
                size=size or None,
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
