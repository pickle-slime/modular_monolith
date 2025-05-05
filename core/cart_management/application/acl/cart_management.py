from ...domain.interfaces.i_acls import *
from ...domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from ..dtos.cart_management import CartDTO, WishlistDTO

import uuid

class CartACL(ICartACL):
    def __init__(self, cart_repository: ICartRepository):
        self.cart_rep = cart_repository

    def fetch_cart(self) -> CartDTO:
        return CartDTO.from_entity(self.cart_rep.fetch_cart())

class WishlistACL(IWishlistACL):
    def __init__(self, wishlist_repository: IWishlistRepository):
        self.wishlist_rep = wishlist_repository

    def fetch_wishlist(self, public_uuid: uuid.UUID | None = None) -> WishlistDTO:
        return WishlistDTO.from_entity(self.wishlist_rep.fetch_wishlist_by_user(public_uuid))
