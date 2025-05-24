from decimal import Decimal
from pydantic import BaseModel, field_validator
import uuid

class AddWishlistItemRequestDTO(BaseModel):
    product: uuid.UUID
    qty: int
    color: str
    size: uuid.UUID

class DeleteWishlistItemRequestDTO(BaseModel):
    item_public_uuid: uuid.UUID
    price: Decimal
    qty: int

#    @field_validator("price", mode="before")
#    def validate_price(cls, value):
#        if isinstance(value, str):
#            value = Decimal(value)
#        return value

    
