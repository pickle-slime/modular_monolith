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
    inner_uuid: uuid.UUID
    public_uuid: uuid.UUID
    color: str = Field(default='Black')
    qty: int = Field(default=0)
    size: uuid.UUID

    @classmethod
    def from_entity(cls, entity: CartItemEntity) -> 'RedisCartItemDTO':
        return cls(
            inner_uuid=entity.inner_uuid,
            public_uuid=entity.public_uuid,
            color=entity.color,
            qty=entity.qty,
            size=entity.size,
        )
    
    def to_entity(self) -> CartItemEntity:
        return CartItemEntity(
            inner_uuid=self.inner_uuid,
            public_uuid=self.public_uuid,
            color=self.color,
            qty=self.qty,
            size=self.size,
        )

class RedisCartDTO(BaseEntityDTO):
    inner_uuid: uuid.UUID
    public_uuid: uuid.UUID
    total_price: float = Field(default=0.0)
    quantity: int = Field(default=0)

    items: list[RedisCartItemDTO] = Field(default_factory=list)

    user: uuid.UUID

    @classmethod
    def from_entity(cls, entity: CartEntity) -> 'RedisCartDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price is not None else 0.0,
            quantity=entity.quantity or 0,
            items=[RedisCartItemDTO.from_entity(value) for value in entity.items.values()] if entity.items else list(),
            user=entity.user,
            inner_uuid=entity.inner_uuid,
            public_uuid=entity.public_uuid,
        )
    
    def to_entity(self) -> CartEntity:
        return CartEntity(
            inner_uuid=self.inner_uuid,
            public_uuid=self.public_uuid,
            total_price=Decimal(self.total_price) if self.total_price else Decimal("0.0"),
            quantity=self.quantity,
            user=self.user,
            items={item.public_uuid: item.to_entity() for item in self.items} if self.items else dict(),
        )
