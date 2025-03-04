from core.utils.application.base_dto import BaseEntityDTO
from core.cart_management.domain.aggregates.cart_management import CartItem as CartItemEntity, Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity

from pydantic import Field
import uuid

class BaseItemDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    color: str = Field(default='Black')
    qty: int = Field(default=0)

    size: uuid.UUID | None = Field(default=None)
    size_snapshot: dict | None = Field(default=None)

class CartItemDTO(BaseItemDTO):
    @staticmethod
    def from_entity(entity: CartItemEntity) -> 'CartItemDTO':
        return CartItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
            size_snapshot=entity.size_snapshot,
        )

class WishlistItemDTO(BaseItemDTO):
    @staticmethod
    def from_entity(entity: WishlistItemEntity) -> 'WishlistItemDTO':
        return WishlistItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
            size_snapshot=entity.size_snapshot,
        )

class BaseItemCollectionDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    total_price: int = Field(default=0)
    quantity: int = Field(default=0)

    items: list[CartItemDTO] = Field(default_factory=list)

    user: uuid.UUID | None = Field(default=None)


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
            user=entity.user,
            pub_uuid=entity.public_uuid,
        )