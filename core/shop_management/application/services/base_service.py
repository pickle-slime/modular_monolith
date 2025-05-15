from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.application.base_service import Service, BaseService as BaseServiceProtocol, BaseTemplateService as BaseTemplateServiceProtocol

from core.shop_management.application.dtos.shop_management import CategoryDTO, ProductDTO
from core.shop_management.application.dtos.acl_dtos import ACLUserDTO, ACLCartDTO, ACLWishlistDTO

from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity

from core.shop_management.domain.interfaces.i_repositories.i_shop_management import ICategoryRepository, IBrandRepository, IProductRepository
from core.cart_management.domain.interfaces.i_acls import ICartACL, IWishlistACL
from core.cart_management.application.acl_exceptions import NotFoundWishlistACLError, NotFoundCartACLError
from core.user_management.domain.interfaces.i_acls import IUserACL
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

from typing import TypeVar
import uuid

T = TypeVar("T", bound=object)

class BaseService(BaseCachingMixin, BaseServiceProtocol[Service]):
    def __init__(
            self, 
            session_adapter: RedisSessionHost | type[RedisSessionHost], 
            user_acl: IUserACL | type[IUserACL],
        ):
        self.session: RedisSessionHost = self._resolve_dependency(session_adapter)
        self.user_acl = self._resolve_dependency(user_acl)
        super().__init__(session_adapter=session_adapter)

    def _resolve_dependency(self, dependency: T | type[T]) -> T:
        """Helper method to instantiate class if type is passed"""
        return dependency() if isinstance(dependency, type) else dependency # pyright: ignore[reportReturnType]

    @property
    def user(self) -> ACLUserDTO:
        if not hasattr(self, "_user"):
            user_public_uuid = self.session.get('user_public_uuid', None)
            user = self.user_acl.fetch_by_uuid(public_uuid=user_public_uuid) if user_public_uuid else self.user_acl.guest()
            self._user = ACLUserDTO.from_user_dto(user)
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
        category_repository: ICategoryRepository,
        cart_acl: ICartACL,
        wishlist_acl: IWishlistACL,

        brand_repository: IBrandRepository,
        product_repository: IProductRepository,
        url_mapping_adapter: URLHost,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.brand_rep = brand_repository
        self.product_rep = product_repository
        self.url_mapping = url_mapping_adapter
        self.category_rep = category_repository
        self.cart_acl = cart_acl
        self.wishlist_acl = wishlist_acl

    def get_header_and_footer(self) -> dict:
        navigation_and_search_bar = [CategoryDTO.from_entity(entity, url_mapping_adapter=self.url_mapping) for entity in self.category_rep.fetch_categories(10, 'count_of_deals')]
        
        self.context['navigation'] = navigation_and_search_bar[:6]
        self.context['breadcrumb'] = self.path.split("/") if self.path else None
        self.context['search_bar'] = navigation_and_search_bar
        self.context['user'] = self.user
        
        if self.is_authorized:
            try:
                self.context['cart'] = self.cart_acl.fetch_cart()
            except NotFoundCartACLError:
                self.context['cart'] = None
                self.context['cart_warning'] = "We couldn't load your cart. It may be empty or not initialized yet."

            try:
                t = ACLWishlistDTO.from_dto(self.wishlist_acl.fetch_wishlist(public_uuid=self.user.pub_uuid))
                self.context['wishlist'] =  t 
            except NotFoundWishlistACLError:
                self.context['wishlist'] = None
                self.context['wishlist_warning'] = "We couldn't load your wishlist. It may be empty or not initialized yet."
        return self.context

    #@BaseCachingMixin.cache_result(key_template="{amount}{indent}", prefix="top_selling", dtos=[ProductDTO])
    def get_top_selling(self, amount=5, indent=0) -> list[ProductDTO]:
        return self.create_product_dtos(self.product_rep.fetch_top_selling(amount, indent))
    
    def create_product_dtos(self, entities: list[ProductEntity]) -> list[ProductDTO]:
        '''
        Creates a list of specific ProductDTO instances
        Populates these instances with a CategoryDTO and a BrandDTO
        '''
        dtos = []
        for entity in entities:
            category = self._fetch_category(entity.category.public_uuid)
            brand = self._fetch_brand(entity.brand.public_uuid)
            dto = ProductDTO.from_entity(entity, category=category, brand=brand, url_mapping_adapter=self.url_mapping).populate_none_fields()
            dtos.append(dto)
        return dtos
    
    def _fetch_category(self, public_uuid: uuid.UUID) -> CategoryEntity | None:
        return self.category_rep.fetch_by_uuid(public_uuid) 

    def _fetch_brand(self, public_uuid: uuid.UUID) -> BrandEntity | None:
        return self.brand_rep.fetch_by_uuid(public_uuid)
