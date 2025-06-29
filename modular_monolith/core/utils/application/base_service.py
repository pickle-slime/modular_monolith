from core.user_management.domain.interfaces.i_repositories.i_user_management import IUserRepository
from core.shop_management.domain.interfaces.i_repositories.i_shop_management import ICategoryRepository
from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository

from core.shop_management.domain.interfaces.i_acls import ICategoryACL
from core.cart_management.domain.interfaces.i_acls import ICartACL, IWishlistACL
from core.user_management.domain.interfaces.i_acls import IUserACL

from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from core.user_management.domain.entities.user_management import User as UserEntity
from core.user_management.application.dtos.user_management import UserDTO

from typing import TypeVar, Protocol, overload

Service = TypeVar("Service", covariant=True)

T = TypeVar("T", bound=object)

class BaseService(Protocol[Service]):
    '''
    Core protocol that is shared across all bounded contexts.
    '''

    #overload for user bounded context
    @overload
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_repository: IUserRepository | type[IUserRepository],
        ):
        pass

    #overload for other bounded contexts
    @overload
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserACL | type[IUserACL],
        ):
        pass

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        ...

    @property
    def user(self) -> UserEntity | UserDTO:
        ...
    
    @property
    def path(self) -> str:
        ...
    
    @property
    def is_authorized(self) -> bool:
        ...


class BaseTemplateService(BaseService[Service], Protocol[Service]):
    '''
    Base service for TempleServices. It handles heander and footer
    '''

    context = dict()

    #overload for shop bounded context
    @overload
    def __init__(
        self, 
        category_repository: ICategoryRepository,
        cart_acl: ICartACL,
        wishlist_acl: IWishlistACL,
    ):
        pass

    #overload for cart bounded context
    @overload
    def __init__(
        self, 
        category_acl: ICategoryACL,
        cart_repository: ICartRepository,
        wishlist_repository: IWishlistRepository,
    ):
        pass

    #overload for other bounded contexts
    @overload
    def __init__(
        self, 
        category_acl: ICategoryACL,
        cart_acl: ICartACL,
        wishlist_acl: IWishlistACL,
    ):
        pass

    def get_header_and_footer(self) -> dict:
        ...
