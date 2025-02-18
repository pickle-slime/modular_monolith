from ...application.dtos.cart_management import CartDTO, WishlistDTO

from abc import ABC, abstractmethod
import uuid

class ICartACL(ABC):
    @abstractmethod
    def fetch_cart(self) -> CartDTO:
        pass

class IWishlistACL(ABC):
    @abstractmethod
    def fetch_wishlist(self, inner_uuid: uuid.UUID = None, public_uuid: uuid.UUID = None) -> WishlistDTO:
        pass