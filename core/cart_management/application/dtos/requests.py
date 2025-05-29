from decimal import Decimal
from pydantic import BaseModel
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

class AddCartItemRequestDTO(BaseModel):
    product: uuid.UUID
    qty: int
    color: str
    size: uuid.UUID

class DeleteCartItemRequestDTO(BaseModel):
    item_public_uuid: uuid.UUID
    price: Decimal
    qty: int
