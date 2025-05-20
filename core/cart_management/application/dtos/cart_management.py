from core.utils.application.base_dto import BaseEntityDTO, BaseDTO, DTO
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO
from core.cart_management.domain.entities.cart_management import Cart as CartEntity

from pydantic import Field, field_validator
from decimal import Decimal
import uuid

class BaseItemDTO(BaseDTO[DTO]):
    color: str | None = Field(default=None, min_length=3, max_length=100, title="Item Color")
    qty: int | None = Field(default=None, ge=0, lt=100, title="QTY", description="QTY per item")
    size: uuid.UUID | None = Field(default=None, title="Size", description="Represents a fereign key in the database")

class CartItemDTO(BaseItemDTO['CartItemDTO']):
    @classmethod
    def from_vo(cls, entity: CartItemVO) -> 'CartItemDTO':
        return cls(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
        )

class WishlistItemDTO(BaseItemDTO['WishlistItemDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None, title="Public UUID")
    @classmethod
    def from_entity(cls, entity: WishlistItemEntity) -> 'WishlistItemDTO':
        return cls(
            pub_uuid=entity.public_uuid,
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
        )

class BaseItemCollectionDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    total_price: float | None = Field(default=None, ge=0, title="Total Price")
    quantity: int | None = Field(default=None, ge=0, title="Quantity")

    user: uuid.UUID | None = Field(default=None, title="User", description="Contains a public uuid of external module")

    @field_validator("total_price", mode="before")
    def validate_total_price(cls, v):
        if isinstance(v, Decimal) or isinstance(v, int):
            return float(v)
        return v

class CartDTO(BaseItemCollectionDTO):
    items: list[CartItemDTO]| None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def from_entity(cls, entity: CartEntity) -> 'CartDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price else None,
            quantity=entity.quantity,
            items=[CartItemDTO.from_vo(item) for item in entity.items] if entity.items else [],
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )
    

class WishlistDTO(BaseItemCollectionDTO):
    items: list[WishlistItemDTO] | None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def from_entity(cls, entity: WishlistEntity) -> 'WishlistDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price is not None else None,
            quantity=entity.quantity,
            items=[WishlistItemDTO.from_entity(entity.items[pub_uuid]) for pub_uuid in entity.items] if entity.items else [],
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )
