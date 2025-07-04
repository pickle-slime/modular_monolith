from time import perf_counter
from typing import Any, Literal
import uuid

from core.shop_management.application.dtos.infrastructure import PaginatedProductsInfDTO
from core.utils.application.base_cache_mixin import BaseCachingMixin 
from core.shop_management.application.services.base_service import BaseTemplateService

from core.review_management.domain.interfaces.i_acl import IProductRatingACL
from core.cart_management.application.acl_exceptions import NotFoundWishlistACLError, NotFoundCartACLError
from core.shop_management.application.exceptions import InvalidFiltersError
from core.shop_management.application.dtos.shop_management import ProductDTO, CategoryDTO, BrandDTO, ProductImageDTO, PaginatedProductsDTO

class HomePageService(BaseTemplateService['HomePageService']):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_hot_deals(self) -> list[ProductDTO]:
        hot_deals = self.product_rep.fetch_hot_deals(30)
        return self.create_product_dtos(hot_deals)
    
    def _get_slick_tablet(self, amount: int) -> list[ProductDTO]:
        slick_tablet = []
        for i in range(0, amount, 3):
            slick_tablet.append(self.get_top_selling(i+3, i))

        return slick_tablet

    @BaseCachingMixin.cache_result("{self.user.pub_uuid}", dtos=[ProductDTO, CategoryDTO])
    def _get_context_data(self) -> dict[str, Any]:
        context = dict()
        context['hot_deals'] = self._get_hot_deals()
        context['top_selling'] = self.get_top_selling(5)
        context['slick_tablet'] = self._get_slick_tablet(6)

        return context
    
    def get_context_data(self) -> dict[str, Any]:
        return {**self.get_header_and_footer(), **self._get_context_data()}

class StorePageService(BaseTemplateService['StorePageService']):
    paginate_by = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_context_data(self, request_data: dict[str, Any]) -> dict[str, Any]:
        context = dict()
        context.update(self.get_header_and_footer())
        context.update(self._fetch_aside_data())
        context.update(self._process_request_data(request_data))

        return context
    
    def _fetch_aside_data(self) -> dict[str, Any]:
        return {
            'category_aside': [CategoryDTO.from_entity(entity).populate_none_fields() for entity in self.category_rep.fetch_categories(limit=6)],
            'brands': [BrandDTO.from_entity(brand).populate_none_fields() for brand in self.brand_rep.fetch_brands(limit=6)],
            'tablet_aside': self.get_top_selling(3),
        }
    
    def _process_request_data(self, request_data: dict[str, Any]) -> dict[str, Any] | dict:
        if request_data.get('method') == "POST":
            return {
                'select_option_sort_by': request_data.get('sort_by'),
                'checkbox_categories': request_data.get('category', []),
                'checkbox_brands': request_data.get('brand', []),
            }
        return {}

    def handle_get_request(self, page: int, category: str | None, query: str | None, navigation: bool = False, category_slug: str | None = None) -> PaginatedProductsDTO:
        if navigation:
            return self.filter_products_by_slug_of_category(page, category_slug)
        elif category or query:
            return self.handle_search(page, self._resolve_category_uuid(category), query)
        return self.get_paginated_products(page)

    def handle_search(self, page: int, category: uuid.UUID | None, query: str | None) -> PaginatedProductsDTO:
        return self.create_paginated_product_dtos(self.product_rep.searching_products(page=page, per_page=self.paginate_by, query=query, category_pub=category))

    def filter_products_by_slug_of_category(self, page: int, category: str | None) -> PaginatedProductsDTO:
        return self.create_paginated_product_dtos(self.product_rep.filter_by_category_slug(page=page, per_page=self.paginate_by, category_slug=category))

    def get_paginated_products(self, page: int) -> PaginatedProductsDTO:
        data = self.get_filters_from_sessions()
        dto: PaginatedProductsDTO = self.filter_products(data, page)
        return dto or self.create_paginated_product_dtos(self.product_rep.fetch_paginated_top_selling(page, per_page=self.paginate_by))
    
    #@BaseCachingMixin.cache_result("{data.category}.{data.brand}", prefix="filter_products", dtos=[ProductDTO])
    def filter_products(self, data: dict[str, Any], page: int) -> PaginatedProductsDTO:
        entities = None
        if data['category'] and data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], page=page, per_page=self.paginate_by, category_pubs=data['category'], brand_pubs=data['brand'])
        elif not data['category'] and not data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], page=page, per_page=self.paginate_by)
        elif not data['category']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], page=page, per_page=self.paginate_by, brand_pubs=data['brand'])
        elif not data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], page=page, per_page=self.paginate_by, category_pubs=data['category'])

        self.set_filters_in_sessions(data)

        if entities:
            return self.create_paginated_product_dtos(entities)
        else:
            raise InvalidFiltersError("incorrect filters")

    def set_filters_in_sessions(self, data: dict[str, Any]):
        self.session_adapter.set("price_min", data['price__min'] or 1.00)
        self.session_adapter.set("price_max", data['price__max'] or 9999.00)
        self.session_adapter.set("sort_by", data['sort_by'] or 'count_of_selled')
        self.session_adapter.set("brand", data['brand'] or None)
        self.session_adapter.set("category", data['category'] or None)

    def get_filters_from_sessions(self) -> dict[str, Any]:
        data = dict()
        data["price__min"] = self.session_adapter.get("price_min", default=1.00)
        data["price__max"] = self.session_adapter.get("price_max", default=9999.00)
        data["sort_by"] = self.session_adapter.get("sort_by", default='count_of_selled')
        data["brand"] = self.session_adapter.get("brand", default=None)
        data["category"] = self.session_adapter.get("category", default=None)
        return data

    def post(self):
        """Whole workflow goes through get_context_data and get_queryset"""
        pass

    def _resolve_category_uuid(self, category: str | None) -> uuid.UUID | None:
        if not category:
            return None
    
        try:
            return uuid.UUID(category)
        except ValueError:
            return None

    def create_paginated_product_dtos(self, inf_dto: PaginatedProductsInfDTO) -> PaginatedProductsDTO:
        '''
        Creates a PaginatedProductsDTO with populated product DTOs
        Populates these instances with a CategoryDTO and a BrandDTO
        '''
        dtos = []
        for entity in inf_dto.products:
            category = self.fetch_category(entity.category.public_uuid)
            brand = self.fetch_brand(entity.brand.public_uuid)
            dto = ProductDTO.from_entity(entity, category=category, brand=brand, url_mapping_adapter=self.url_mapping).populate_none_fields()
            dtos.append(dto)
        return PaginatedProductsDTO.from_populated_dtos(inf_dto, dtos)
    
class ProductPageService(BaseTemplateService['ProductPageService']):
    def __init__(
            self, 
            product_rating_acl: IProductRatingACL,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.product_rating_acl = product_rating_acl

    #@BaseCachingMixin.cache_result("get_object_{url_parameters}")
    def get_object(self, url_parameters: Any) -> ProductDTO:
        category_slug = url_parameters.get('category', None)
        product_slug = url_parameters.get('product', None)

        self.entity = self.product_rep.fetch_by_slugs(product_slug=product_slug, category_slug=category_slug)
        return ProductDTO.from_entity(
            self.entity,
            self.category_rep.fetch_by_uuid(self.entity.category.public_uuid),
            self.brand_rep.fetch_by_uuid(self.entity.brand.public_uuid),
            url_mapping_adapter=self.url_mapping,
        )

    def get_context_data(self) -> dict[str, Any]:
        header_and_footer = self.get_header_and_footer()
        product_rating_dto = self.product_rating_acl.fetch_rating_by_product_uuid(self.entity.public_uuid)
        
        context = dict()
        context['product_images'] = ProductImageDTO.from_entities(self.entity.images)
        context['related_products'] = self.create_product_dtos(self.product_rep.fetch_related_products(brand=self.entity.brand.inner_uuid, limit=10, select_related='category'))
        context['product_rating'] = product_rating_dto.populate_none_fields()
        context['stars'], context['reviews_avg'] = self.product_rating_acl.fetch_rating_product_stars(product_rating_dto.pub_uuid)
        context['reviews_count'] = self.product_rating_acl.fetch_reviews_count(product_rating_dto.pub_uuid)


        if self.user.is_authenticated:
            try:
                context['add_wishlist'] = self.wishlist_acl.fetch_wishlist(self.user.pub_uuid) if self.user.pub_uuid else None
            except (NotFoundWishlistACLError):
                context["add_wishlist"] = None
                context["wishlist_error"] = "We couldn't load your wishlist. It may be empty or not initialized yet."
            
            try:
                context['add_cart'] = self.cart_acl.fetch_cart()
            except (NotFoundCartACLError):
                context["add_cart"] = None
                context["cart_error"] = "We couldn't load your cart. It may be empty or not initialized yet."

        return {**header_and_footer, **context}

    def post(self) -> None:
        pass

