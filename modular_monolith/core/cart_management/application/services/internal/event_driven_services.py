from core.cart_management.application.dtos.acl_event_driven_dtos import LoggedUserEventDTO, SignedUPUserEventDTO
from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from core.cart_management.domain.aggregates.cart_management import Cart as CartEntity, Wishlist as WishlistEntity
from core.cart_management.application.exceptions import InvalidSessionAdapter, FailedCartInitializationError, FailedWishlistInitializationError

class UserManagementService:
    def __init__(self, cart_repository: ICartRepository | None = None, wishlist_repository: IWishlistRepository | None = None):
        self.cart_repo = cart_repository
        self.wishlist_repo = wishlist_repository

    def handle_logged_user(self, dto: LoggedUserEventDTO) -> None:
        empty_cart = CartEntity(user=dto.pub_uuid)
        try:
            if self.cart_repo:
                self.cart_repo.save(empty_cart)
            else:
                raise FailedCartInitializationError("Missing cart repository")
        except (InvalidSessionAdapter, FailedCartInitializationError) as e:
            raise FailedCartInitializationError(f"Failed to initiate a cart, cause:\n{e.raw_msg}")

    def handle_registered_user(self, dto: SignedUPUserEventDTO) -> None:
        empty_wishlist = WishlistEntity(user=dto.pub_uuid)
        try:
            if self.wishlist_repo:
                self.wishlist_repo.save(empty_wishlist)
            else:
                raise FailedWishlistInitializationError("Missing wishlist repository")
        except (InvalidSessionAdapter, FailedWishlistInitializationError) as e:
            raise FailedCartInitializationError(f"Failed to initiate a wishlist, cause:\n{e.raw_msg}")

