from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.application.base_service import Service, BaseTemplateService

from core.shop_management.application.dtos.shop_management import CategoryDTO
from core.cart_management.application.dtos.cart_management import CartDTO, WishlistDTO
from core.user_management.application.dtos.user_management import UserDTO

from core.shop_management.domain.interfaces.i_repositories.i_shop_management import ICategoryRepository
from core.cart_management.domain.interfaces.i_acls import ICartACL, IWishlistACL
from core.user_management.domain.interfaces.i_acls import IUserACL
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from typing import TypeVar, Generic

T = TypeVar("T")

class BaseService(Generic[Service]):
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserACL | type[IUserACL],
        ) -> 'BaseService':
        
        self.session = self._resolve_dependency(session_adapter)
        self.user_acl = self._resolve_dependency(user_acl)

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        return dependency() if isinstance(dependency, type) else dependency

    @property
    def user(self):
        if not hasattr(self, "_user"):
            user_public_uuid = self.session.get('user_public_uuid', None)
            self._user = self.user_acl.fetch_by_uuid(public_uuid=user_public_uuid)
        return self._user
    
    @property
    def path(self):
        if not hasattr(self, "_path"):
            self._path = self.session.get('path')
        return self._path
    
    @property
    def is_authorized(self):
        if not hasattr(self, "_is_authorized"):
            self._is_authorized = self.session.get('is_authorized', False)
        return self._is_authorized
    

class BaseTemplateService(BaseService["BaseTemplateService"]):
    '''
    Base service for TempleServices. It handles heander and footer
    '''
    context = dict()

    def __init__(
        self, 
        category_repository: ICategoryRepository,
        cart_acl: ICartACL,
        wishlist_acl: IWishlistACL,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.category_rep = category_repository
        self.cart_acl = cart_acl
        self.wishlist_acl = wishlist_acl

    def get_header_and_footer(self) -> dict:
        navigation_and_search_bar = [CategoryDTO.from_entity(entity) for entity in self.category_rep.fetch_categories(10, 'count_of_deals')]
        
        self.context['navigation'] = navigation_and_search_bar[:6]
        self.context['breadcrumb'] = self.path.split("/") if self.path else None
        self.context['search_bar'] = navigation_and_search_bar
        self.context['user'] = self.user
        
        if self.is_authorized:
            self.context['cart'] = CartDTO.from_entity(self.cart_acl.fetch_cart())#CartOrderProduct.objects.filter(cart=request.user.cart.pk).select_related('size__product__category')
            self.context['wishlist'] = WishlistDTO.from_entity(self.wishlist_acl.fetch_wishlist(public_uuid=self.user.uuid)) #WishListOrderProduct.objects.filter(wishlist=request.user.wishlist.pk).select_related('size__product__category')
        return self.context
