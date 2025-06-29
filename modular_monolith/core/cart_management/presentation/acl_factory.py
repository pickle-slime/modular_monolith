from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from ..infrastructure.repositories.cart_management import DjangoCartRepository, DjangoWishlistRepository
from ..application.acl.cart_management import CartACL, WishlistACL

class CartManagementACLFactory:
    @staticmethod
    def create_cart_acl(session_host: RedisSessionHost) -> CartACL:
        return CartACL(cart_repository=DjangoCartRepository(session_host))
    
    @staticmethod
    def create_wishlist_acl() -> WishlistACL:
        return WishlistACL(DjangoWishlistRepository())