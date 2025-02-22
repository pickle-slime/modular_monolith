from abc import abstractmethod

from .....utils.domain.interfaces.i_repositories.base_repository import BaseRepository
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity, Cart as CartEntity

import uuid

class IWishlistRepository(BaseRepository):
    @abstractmethod
    def fetch_wishlist_by_user(self, public_uuid: uuid.UUID = None) -> WishlistEntity:
        pass

class IWishlistItemRepository(BaseRepository):
    pass

class ICartRepository(BaseRepository):
    @abstractmethod
    def fetch_cart(self) -> CartEntity:
        pass
 
class ICartItemRepository(BaseRepository):
    pass