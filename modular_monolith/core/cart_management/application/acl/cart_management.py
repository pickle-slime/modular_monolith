from core.cart_management.application.exceptions import NotFoundWishlistError, NotFoundCartError 
from core.cart_management.application.acl_exceptions import NotFoundWishlistACLError, NotFoundCartACLError
from ...domain.interfaces.i_acls import *
from ...domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from ..dtos.cart_management import CartDTO, WishlistDTO

import uuid

class CartACL(ICartACL):
    def __init__(self, cart_repository: ICartRepository):
        self.cart_rep = cart_repository

    def fetch_cart(self) -> CartDTO:
        try:
            return CartDTO.from_entity(self.cart_rep.fetch_cart())
        except NotFoundCartError:
            raise NotFoundCartACLError(f"didnt find cart by session key ({self.cart_rep.session_key})")

class WishlistACL(IWishlistACL):
    def __init__(self, wishlist_repository: IWishlistRepository):
        self.wishlist_rep = wishlist_repository

    def fetch_wishlist(self, public_uuid: uuid.UUID) -> WishlistDTO:
        try:
            return WishlistDTO.from_entity(self.wishlist_rep.fetch_wishlist_by_user(public_uuid))
        except NotFoundWishlistError:
            raise NotFoundWishlistACLError(f"didnt find wishlist by user public uuid ({public_uuid})")
