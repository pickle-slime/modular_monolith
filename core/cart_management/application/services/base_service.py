from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.application.base_service import Service, BaseService as BaseServiceProtocol, BaseTemplateService as BaseTemplateServiceProtocol

from core.cart_management.application.dtos.acl_dtos import ACLUserDTO

from core.shop_management.domain.interfaces.i_acls import ICategoryACL
from core.user_management.domain.interfaces.i_acls import IUserACL
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from typing import TypeVar

T = TypeVar("T", bound=object)

class BaseService(BaseCachingMixin, BaseServiceProtocol[Service]):
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserACL | type[IUserACL],
            *args,
            **kwargs
        ):
        
        self.session = self._resolve_dependency(session_adapter)
        self.user_acl = self._resolve_dependency(user_acl)
        super().__init__(session_adapter=session_adapter, *args, **kwargs)

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        return dependency() if isinstance(dependency, type) else dependency

    @property
    def user(self) -> ACLUserDTO:
        if not hasattr(self, "_user"):
            user_public_uuid = self.session.get('user_public_uuid', None)
            self._user = ACLUserDTO.from_user_dto(self.user_acl.fetch_by_uuid(public_uuid=user_public_uuid)) if user_public_uuid else ACLUserDTO.from_user_dto(self.user_acl.guest())
        return self._user
    
    @property
    def path(self) -> str:
        if not hasattr(self, "_path"):
            self._path = self.session.get('path')
        return self._path
    
    @property
    def is_authorized(self) -> bool:
        if not hasattr(self, "_is_authorized"):
            self._is_authorized = self.session.get('is_authorized', False)
        return self._is_authorized
    

class BaseTemplateService(BaseService, BaseTemplateServiceProtocol[Service]):
    '''
    Base service for TempleServices. It handles heander and footer
    '''
    context = dict()

    def __init__(
        self, 
        category_acl: ICategoryACL,
        cart_repository: ICartRepository,
        wishlist_repository: IWishlistRepository,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.category_acl = category_acl
        self.cart_repository = cart_repository
        self.wishlist_repository = wishlist_repository

    def get_header_and_footer(self) -> dict:
        navigation_and_search_bar = self.category_acl.fetch_categories(10, 'count_of_deals')
        
        self.context['navigation'] = navigation_and_search_bar[:6]
        self.context['breadcrumb'] = self.path.split("/") if self.path else None
        self.context['search_bar'] = navigation_and_search_bar
        self.context['user'] = self.user
        
        if self.is_authorized:
            self.context['cart'] = self.cart_repository.fetch_cart()
            self.context['wishlist'] = self.wishlist_repository.fetch_wishlist_by_user(public_uuid=self.user.pub_uuid)
        return self.context
