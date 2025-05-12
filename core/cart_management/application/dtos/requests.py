from pydantic import BaseModel
import uuid

class AddWishlistItemRequestDTO(BaseModel):
    product: uuid.UUID
    qty: int
    color: str
    size: uuid.UUID

    
