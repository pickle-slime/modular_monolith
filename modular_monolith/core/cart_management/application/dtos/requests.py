from pydantic import BaseModel, Field
import uuid

class AddWishlistItemRequestDTO(BaseModel):
    product: uuid.UUID
    size: uuid.UUID | None = Field(default=None)
    color: str | None = Field(default=None)
    qty: int = Field(default=1)

class DeleteWishlistItemRequestDTO(BaseModel):
    item_public_uuid: uuid.UUID
    product: uuid.UUID

class AddCartItemRequestDTO(BaseModel):
    product: uuid.UUID
    size: uuid.UUID | None = Field(default=None)
    color: str | None = Field(default=None)
    qty: int = Field(default=1)

class DeleteCartItemRequestDTO(BaseModel):
    item_public_uuid: uuid.UUID
    product: uuid.UUID
