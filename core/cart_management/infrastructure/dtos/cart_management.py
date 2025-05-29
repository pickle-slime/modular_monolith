from core.cart_management.application.dtos.base_dto import BaseEntityDTO
from core.cart_management.domain.aggregates.cart_management import Cart as CartEntity
from core.cart_management.domain.entities.cart_management import CartItem as CartItemEntity

from pydantic import Field
from decimal import Decimal
import uuid

'''
The DTOs below represent data from external storages.
'''

class RedisCartItemDTO(BaseEntityDTO):
    color: str | None = Field(default='Black')
    qty: int | None = Field(default=0)
    size: uuid.UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls, entity: CartItemEntity) -> 'RedisCartItemDTO':
        return cls(
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
        )
    
    def to_entity(self) -> CartItemEntity:
        return CartItemEntity(
            color=self.color,
            qty=self.qty,
            size=self.size,
        )

class RedisCartDTO(BaseEntityDTO):
    inner_uuid: uuid.UUID = Field(default=None)
    public_uuid: uuid.UUID = Field(default=None)
    total_price: float | None = Field(default=0)
    quantity: int | None = Field(default=0)

    items: dict[uuid.UUID, RedisCartItemDTO] | None = Field(default_factory=dict)

    user: uuid.UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls, entity: CartEntity) -> 'RedisCartDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price is not None else 0.0,
            quantity=entity.quantity,
            items={key: RedisCartItemDTO.from_entity(value) for key, value in entity.items.items()} if entity.items else dict(),
            user=entity.user,
            inner_uuid=entity.inner_uuid,
            public_uuid=entity.public_uuid,
        )
    
    def to_entity(self) -> CartEntity:
        return CartEntity(
            inner_uuid=self.inner_uuid,
            public_uuid=self.public_uuid,
            total_price=Decimal(self.total_price) if self.total_price else None,
            quantity=self.quantity,
            user=self.user,
            items={key: value.to_entity() for key, value in self.items.items()} if self.items else None,
        )
