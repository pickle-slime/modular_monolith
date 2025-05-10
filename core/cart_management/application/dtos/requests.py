from pydantic import BaseModel
import uuid

class AddWishlistItemRequestDTO(BaseModel):
    product: uuid.UUID
    qty: int
    color: str
    size: uuid.UUID

    def map_into_tuple(self) -> tuple[uuid.UUID, int, str, uuid.UUID]:
        return (self.product, self.qty, self.color, self.size)
