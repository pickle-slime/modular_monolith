from core.utils.application.base_dto import BaseEntityDTO, BaseDTO, DTO
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO, Size as SizeVO
from core.cart_management.domain.entities.cart_management import Cart as CartEntity, Size as SizeEntity

from typing import Union
from pydantic import Field, field_validator
from decimal import Decimal
import uuid

class SizeDTO(BaseDTO['SizeDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None)
    length: Decimal | None = Field(default=None, title="Length")
    width: Decimal | None = Field(default=None, title="Width")
    height: Decimal | None = Field(default=None, title="Height")
    weight: Decimal | None = Field(default=None, title="Weight")

    @classmethod
    def from_size_vo(cls, size: SizeVO | None) -> Union['SizeDTO', None]:
        if size is None: return None
        return cls(
            length=size.length,
            width=size.width,
            height=size.height,
            weight=size.weight,
        )

    @classmethod
    def from_size_entity(cls, size: SizeEntity | None) -> Union['SizeDTO', None]:
        if size is None: return None
        return cls(
            pub_uuid=size.public_uuid,
            length=size.length,
            width=size.width,
            height=size.height,
            weight=size.weight,
        )


class BaseItemDTO(BaseDTO[DTO]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    color: str | None = Field(default=None, min_length=3, max_length=100, title="Item Color")
    qty: int | None = Field(default=None, ge=0, lt=100, title="QTY", description="QTY per item")

    size_snapshot: SizeDTO | None = Field(default=None, title="Size Snapshot", description="Contains a DTO of size value object")

class CartItemDTO(BaseItemDTO['CartItemDTO']):
    @classmethod
    def from_vo(cls, entity: CartItemVO) -> 'CartItemDTO':
        return cls(
            color=entity.color,
            qty=entity.qty,
            size_snapshot=SizeDTO.from_size_vo(entity.size),
        )

class WishlistItemDTO(BaseItemDTO['WishlistItemDTO']):
    size: uuid.UUID | None = Field(default=None, title="Size", description="Contatins the public uuid of external module")

    @staticmethod
    def from_entity(entity: WishlistItemEntity) -> 'WishlistItemDTO':
        return WishlistItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size.public_uuid if entity.size else None,
            size_snapshot=SizeDTO.from_size_entity(entity.size),
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
            items=[CartItemDTO.from_vo(entity.items[pub_uuid]) for pub_uuid in entity.items] if entity.items else [],
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )
    

class WishlistDTO(BaseItemCollectionDTO):
    items: list[WishlistItemDTO]| None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def from_entity(cls, entity: WishlistEntity) -> 'WishlistDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price else None,
            quantity=entity.quantity,
            items=[WishlistItemDTO.from_entity(entity.items[pub_uuid]) for pub_uuid in entity.items] if entity.items else [],
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )
