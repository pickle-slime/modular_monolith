from ...application.dtos.cart_management import CartDTO, WishlistDTO

from abc import ABC, abstractmethod
import uuid

class ICartACL(ABC):
    @abstractmethod
    def fetch_cart(self) -> CartDTO:
        pass

class IWishlistACL(ABC):
    @abstractmethod
    def fetch_wishlist(self, public_uuid: uuid.UUID) -> WishlistDTO:
        pass
