from core.utils.application.base_dto import BaseEntityDTO
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO

from pydantic import Field
from decimal import Decimal
import uuid

'''
The DTOs below represent data from external storages.
'''

class RedisCartItemDTO(BaseEntityDTO):
    color: str | None = Field(default='Black')
    image: str | None = Field(default=None)
    price: float | None = Field(default=None)

    qty: int | None = Field(default=0)

    size: uuid.UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls, entity: CartItemVO) -> 'RedisCartItemDTO':
        return cls(
            color=entity.color,
            image=entity.image,
            price=float(entity.price) if entity.price is not None else None,
            qty=entity.qty,
            size=entity.size,
        )
    
    def to_entity(self) -> CartItemVO:
        return CartItemVO(
            color=self.color,
            image=self.image,
            price=Decimal(self.price) if self.price is not None else None,
            qty=self.qty,
            size=self.size,
        )

class RedisCartDTO(BaseEntityDTO):
    inner_uuid: uuid.UUID = Field(default=None)
    public_uuid: uuid.UUID = Field(default=None)
    total_price: float | None = Field(default=0)
    quantity: int | None = Field(default=0)

    items: list[RedisCartItemDTO] | None = Field(default_factory=list)

    user: uuid.UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls, entity: CartEntity) -> 'RedisCartDTO':
        return cls(
            total_price=float(entity.total_price) if entity.total_price is not None else 0.0,
            quantity=entity.quantity,
            items=[RedisCartItemDTO.from_entity(item) for item in entity.items] if entity.items else [],
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
            items=[item.to_entity() for item in self.items] if self.items else None
        )
