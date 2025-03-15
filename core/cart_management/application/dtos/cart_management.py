from core.utils.application.base_dto import BaseEntityDTO, BaseDTO, DTO
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO, Size as SizeVO
from core.cart_management.domain.entities.cart_management import Cart as CartEntity

from pydantic import Field
from decimal import Decimal
import uuid

class SizeDTO(BaseDTO['SizeDTO']):
    length: Decimal | None = Field(default=None, title="Length")
    width: Decimal | None = Field(default=None, title="Width")
    height: Decimal | None = Field(default=None, title="Height")
    weight: Decimal | None = Field(default=None, title="Weight")

    @staticmethod
    def from_size_vo(size: SizeVO) -> 'SizeDTO':
        '''maps the external dto'''
        return SizeDTO(
            length=size.length,
            width=size.width,
            height=size.height,
            weight=size.weight,
        )

class BaseItemDTO(BaseEntityDTO[DTO]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    color: str | None = Field(default=None, min_length=3, max_length=100, title="Item Color")
    qty: int | None = Field(default=None, ge=0, lt=100, title="QTY", description="QTY per item")

    size: uuid.UUID | None = Field(default=None, title="Size", description="Contatins the public uuid of external module")
    size_snapshot: SizeDTO | None = Field(default=None, title="Size Snapshot", description="Contains a DTO of size value object")

class CartItemDTO(BaseItemDTO['CartItemDTO']):
    @staticmethod
    def from_entity(entity: CartItemVO) -> 'CartItemDTO':
        return CartItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
            size_snapshot=SizeDTO.from_size_vo(entity.size),
        )

class WishlistItemDTO(BaseItemDTO['WishlistItemDTO']):
    @staticmethod
    def from_entity(entity: WishlistItemEntity) -> 'WishlistItemDTO':
        return WishlistItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
            size_snapshot=SizeDTO.from_size_vo(entity.size),
        )

class BaseItemCollectionDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    total_price: float | None = Field(default=None, ge=0, title="Total Price")
    quantity: int | None = Field(default=None, ge=0, title="Quantity")

    items: list[CartItemDTO]| None = Field(default=None, title="Contains a list of item DTOs")

    user: uuid.UUID | None = Field(default=None, title="User", description="Contains a public uuid of external module")


class CartDTO(BaseItemCollectionDTO):
    @staticmethod
    def from_entity(entity: CartEntity) -> 'CartDTO':
        return CartDTO(
            total_price=entity.total_price,
            quantity=entity.quantity,
            items=[CartItemDTO.from_entity(item) for item in entity.items] if entity.items else [],
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )
    

class WishlistDTO(BaseItemCollectionDTO):
    @staticmethod
    def from_entity(entity: WishlistEntity) -> 'WishlistDTO':
        return WishlistDTO(
            total_price=entity.total_price,
            quantity=entity.quantity,
            items=[WishlistItemDTO.from_entity(item) for item in entity.items] if entity.items else [],
            user=entity.user.public_uuid,
            pub_uuid=entity.public_uuid,
        )