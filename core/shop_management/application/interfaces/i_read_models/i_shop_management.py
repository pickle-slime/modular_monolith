from core.shop_management.application.dtos.acl_dtos import ACLWishlistItemDTO, ACLCartItemDTO
from core.shop_management.application.dtos.composition import WishlistItemDetailsDTO, CartItemDetailsDTO

from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository

from abc import abstractmethod


class IProductReadModel(BaseRepository):
    @abstractmethod
    def fetch_wishlist_items_details(self, items: list[ACLWishlistItemDTO]) -> list[WishlistItemDetailsDTO]:
        pass

    @abstractmethod
    def fetch_cart_items_details(self, items: list[ACLCartItemDTO]) -> list[CartItemDetailsDTO]:
        pass
