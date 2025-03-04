from core.utils.application.base_dto import BaseEntityDTO
from core.cart_management.domain.aggregates.cart_management import CartItem as CartItemEntity, Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity

from pydantic import Field
import uuid

'''
The DTOs below represent data from external storages.
'''

class RedisCartItemDTO(BaseEntityDTO):
    public_uuid: uuid.UUID | None = Field(default=None)
    color: str = Field(default='Black')
    qty: int = Field(default=0)

    size: uuid.UUID | None = Field(default=None)
    size_snapshot: dict | None = Field(default=None)

    @staticmethod
    def from_entity(entity: CartItemEntity) -> 'RedisCartItemDTO':
        return RedisCartItemDTO(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
            size_snapshot=entity.size_snapshot,
        )
    
    def to_entity(self) -> CartItemEntity:
        return RedisCartItemDTO(
            public_uuid=self.public_uuid,
            color=self.color,
            qty=self.qty,
            size=self.size,
            size_snapshot=self.size_snapshot,
        )

class RedisCartDTO(BaseEntityDTO):
    public_uuid: uuid.UUID | None = Field(default=None)
    total_price: int = Field(default=0)
    quantity: int = Field(default=0)

    items: list[RedisCartItemDTO] = Field(default_factory=list)

    user: uuid.UUID | None = Field(default=None)

    @staticmethod
    def from_entity(entity: CartEntity) -> 'RedisCartDTO':
        return RedisCartDTO(
            total_price=entity.total_price,
            quantity=entity.quantity,
            items=[RedisCartItemDTO.from_entity(item) for item in entity.items] if entity.items else [],
            user=entity.user,
            pubic_uuid=entity.public_uuid,
            inner_uuid=entity.inner_uuid,
        )
    
    def to_entity(self) -> CartEntity:
        return CartEntity(
            public_uuid=self.public_uuid,
            total_price=self.total_price,
            quantity=self.quantity,
            user=self.user,
            items=[item.to_entity() for item in self.items]
        )