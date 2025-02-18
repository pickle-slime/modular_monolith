from .base_cache_mixin import BaseCachingMixin

from core.user_management.domain.interfaces.i_repositories.i_user_management import IUserRepository

from core.user_management.domain.interfaces.i_acls import IUserACL
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from typing import TypeVar, Generic, Protocol, overload

Service = TypeVar("Service")

T = TypeVar("T")

class BaseService(Generic[Service], Protocol):
    @overload
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserACL | type[IUserACL],
        ) -> 'BaseService':
        pass

    @overload
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserRepository | type[IUserRepository],
        ) -> 'BaseService':
        pass

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        pass

    @property
    def user(self):
        pass
    
    @property
    def path(self):
        pass
    
    @property
    def is_authorized(self):
        pass


TemplateService = TypeVar("TemplateService", bound="BaseTemplateService")

class BaseTemplateService(BaseService["BaseTemplateService"]):
    '''
    Base service for TempleServices. It handles heander and footer
    '''
    context = dict()

    # def __init__(
    #     self, 
    #     category_acl: ICategoryACL,
    #     cart_acl: ICartACL,
    #     wishlist_acl: IWishlistACL,
    #     **kwargs,
    # ):
    #     pass

    def get_header_and_footer(self) -> dict:
        pass
