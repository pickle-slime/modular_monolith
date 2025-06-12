from core.cart_management.infrastructure.dtos.event_driven_dtos import LoggedUserEventDTO
from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository
from core.cart_management.domain.aggregates.cart_management import Cart as CartEntity
from core.cart_management.application.exceptions import InvalidSessionAdapter, FailedCartInitializationError

class UserManagementService:
    def __init__(self, cart_repository: ICartRepository):
        self.cart_repo = cart_repository

    def handle_logged_user(self, dto: LoggedUserEventDTO) -> None:
        empty_cart = CartEntity(user=dto.pub_uuid)
        try:
            self.cart_repo.save(empty_cart)
        except InvalidSessionAdapter as e:
            raise FailedCartInitializationError(f"Failed to initiate a cart, cause:\n{e.raw_msg}")
