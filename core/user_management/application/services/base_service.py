from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.application.base_service import Service

from core.shop_management.domain.interfaces.i_acls import ICategoryACL
from core.cart_management.domain.interfaces.i_acls import ICartACL, IWishlistACL
from core.user_management.domain.interfaces.i_repositories.i_user_management import IUserRepository
from core.user_management.domain.entities.user_management import User as UserEntity
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

from core.user_management.domain.interfaces.hosts.jwtoken import TokenHost
from core.user_management.domain.interfaces.hosts.password_hasher import PasswordHasherHost

from typing import TypeVar, Generic, Any

T = TypeVar("T", bound=object)

class BaseService(Generic[Service]):
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_repository: IUserRepository | type[IUserRepository],
        ):
        
        self.session = self._resolve_dependency(session_adapter)
        self.user_rep = self._resolve_dependency(user_repository)

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        return dependency if isinstance(dependency, type) else dependency

    @property
    def user(self) -> UserEntity:
        if not hasattr(self, "_user"):
            user_public_uuid = self.session.get('user_public_uuid', None)
            self._user = self.user_rep.find_by_uuid(public_uuid=user_public_uuid)
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
    

class BaseTemplateService(BaseService[Service], BaseCachingMixin):
    '''
    Base service for TempleServices. It handles heander and footer
    '''
    context = dict()

    def __init__(
        self, 
        category_acl: ICategoryACL,
        cart_acl: ICartACL,
        wishlist_acl: IWishlistACL,

        password_hasher_adapter: PasswordHasherHost,
        token_adapter: TokenHost,
        url_mapping_adapter: URLHost,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.category_acl = category_acl
        self.cart_acl = cart_acl
        self.wishlist_acl = wishlist_acl

        self.password_hasher = password_hasher_adapter
        self.token_adapter = token_adapter
        self.url_mapping_adapter = url_mapping_adapter

    def get_header_and_footer(self) -> dict:
        navigation_and_search_bar = self.category_acl.fetch_categories(10, 'count_of_deals', url_mapping_adapter=self.url_mapping_adapter)

        self.context['navigation'] = navigation_and_search_bar[:6]
        self.context['breadcrumb'] = self.path.split("/") if self.path else None
        self.context['search_bar'] = navigation_and_search_bar
        self.context['user'] = self.user
        
        if self.is_authorized:
            self.context['cart'] = self.cart_acl.fetch_cart()
            self.context['wishlist'] = self.wishlist_acl.fetch_wishlist(public_uuid=self.user.public_uuid)
        return self.context
    
    def authenticate(self, email, password) -> tuple[str, str]:
        ''' Returns refresh token and access token accordingly '''
        user = self.user_rep.find_by_email(email)
        if not user or not user.check_password(password, self.password_hasher):
            raise ValueError("Invalid credentials")
        refresh_token = self.token_adapter.refresh_token(user.public_uuid)
        access_token = self.token_adapter.generate_access_token(user.public_uuid)
        return refresh_token, access_token
    
    def get_context_data(self, context: dict[str, Any]) -> dict[str, Any]:
        return {**self.get_header_and_footer(), **context}
