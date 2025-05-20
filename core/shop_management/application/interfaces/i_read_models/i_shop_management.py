from core.shop_management.application.dtos.acl_dtos import ACLWishlistItemDTO
from core.shop_management.application.dtos.composition import WishlistItemDetailsDTO

from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository

from abc import abstractmethod


class IProductReadModel(BaseRepository):
    @abstractmethod
    def fetch_wishlist_items_details(self, items: list[ACLWishlistItemDTO]) -> list[WishlistItemDetailsDTO]:
        pass
