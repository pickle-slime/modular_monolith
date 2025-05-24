from core.user_managment.application.dtos.base_dto import BaseDTO

from core.cart_management.application.dtos.cart_management import CartDTO, WishlistDTO

from pydantic import Field
from decimal import Decimal

class ACLCartDTO(BaseDTO["ACLCartDTO"]):
    length: Decimal | None = Field(default=None, title="Length")
    width: Decimal | None = Field(default=None, title="Width")
    height: Decimal | None = Field(default=None, title="Height")
    weight: Decimal | None = Field(default=None, title="Weight")

    @classmethod
    def from_cart_dto(cls, cart_dto: CartDTO) -> "ACLCartDTO":
        return cls()

class ACLWishlistDTO(BaseDTO["ACLWishlistDTO"]):

    @classmethod
    def from_wishlist_dto(cls, wishlist_dto: WishlistDTO) -> "ACLWishlistDTO":
        return cls()
