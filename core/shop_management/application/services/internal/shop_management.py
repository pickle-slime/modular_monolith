from django.http import HttpRequest

from typing import Any, Union,Generic


from core.cart_management.presentation.cart_management.forms import AddToCartForm

from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.application.base_service import TemplateService
from ..base_service import BaseTemplateService
from core.shop_management.domain.interfaces.i_repositories.i_shop_management import *
from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewRepository, IReviewReadModel
from core.shop_management.application.dtos.shop_management import *
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.review_management.application.dtos.review_management import ProductRatingDTO


class BaseShopTemplateService(Generic[TemplateService], BaseCachingMixin):
    def __init__(
        self, 
        template_service: BaseTemplateService,
        #category_repository: ICategoryRepository,
        brand_repository: IBrandRepository,
        product_repository: IProductRepository,
        url_mapping_adapter: URLHost,
    ):
        self.template_service = template_service
        #self.category_rep = category_repository
        self.brand_rep = brand_repository
        self.product_rep = product_repository
        self.url_mapping = url_mapping_adapter
    
    #@BaseCachingMixin.cache_result(key_template="top_selling_{amount}_{indent}", dtos=[ProductDTO])
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
            dto = ProductDTO.from_entity(entity, category=category, brand=brand, url_mapping_adapter=self.url_mapping)
            dtos.append(dto)
        return dtos
    
    def _fetch_category(self, public_uuid: uuid.UUID) -> CategoryEntity | None:
        return self.template_service.category_rep.fetch_by_uuid(public_uuid) 

    def _fetch_brand(self, public_uuid: uuid.UUID) -> BrandEntity | None:
        return self.brand_rep.fetch_by_uuid(public_uuid)



class HomePageService(BaseShopTemplateService):
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

    @BaseCachingMixin.cache_result("{self.template_service.user.uuid}", dtos=[ProductDTO, CategoryDTO])
    def _get_context_data(self) -> dict[str: Any]:
        context = dict()
        context['hot_deals'] = self._get_hot_deals()
        context['top_selling'] = self.get_top_selling(5)
        context['slick_tablet'] = self._get_slick_tablet(6)

        return context
    
    def get_context_data(self) -> dict[str: Any]:
        return {**self.template_service.get_header_and_footer(), **self._get_context_data()}

class StorePageService(BaseShopTemplateService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_context_data(self, request_data: dict[str: Any], context: dict[str: Any]) -> dict[str: Any]:
        context.update(self.template_service.get_header_and_footer())
        context.update(self._fetch_aside_data())
        context.update(self._process_request_data(request_data))

        return context
    
    def _fetch_aside_data(self) -> dict[str: Any]:
        return {#'filters_aside': form_class,
            'category_aside': self.get_cached_entities("category_aside", [CategoryDTO.from_entity(entity) for entity in self.template_service.category_rep.fetch_categories(limit=6)]),
            'brands': [BrandDTO.from_entity(brand) for brand in self.brand_rep.fetch_brands(limit=6)],
            'tablet_aside': self.get_top_selling(3),
        }
    
    def _process_request_data(self, request_data: dict[str: Any]) -> Union[dict[str: Any], dict[None]]:
        if request_data.get('method') == "POST":
            return {
                'select_option_sort_by': request_data.get('sort_by'),
                'checkbox_categories': request_data.get('category', []),
                'checkbox_brands': request_data.get('brand', []),
            }
        return {}

    def get_session_data(self):
            return {
                "query": self.template_service.session.get("search-query"),
                "category_id": self.template_service.session.pop("search-category", "0"),
            }

    def clear_session_data(self):
        self.template_service.session.pop("search-query")
        self.template_service.session.pop("search-category", "0")

    def handle_get_request(self, **kwargs) -> list[ProductDTO]:
        self.clear_session_data()
        if kwargs:
            return self._filter_products_by_slug_of_category(**kwargs)
        return self.get_top_selling()

    def handle_session_data(self, session_data) -> list[ProductDTO]:
        query = session_data["query"]
        category_inner_uuid = session_data["category_public_uuid"]
        
        if query or category_inner_uuid:
            return self.create_product_dtos(self.product_rep.searching_products(name=query, category_inner=category_inner_uuid))
        
        return self.get_top_selling()
    
    @BaseCachingMixin.cache_result("filter_products_{data.category}_{data.brand}", dtos=[ProductDTO])
    def filter_products(self, data: dict[str, Any]) -> list[ProductDTO]:
        if data['category'] and data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], category_pubs=data['category'], brand_pubs=data['brand'])
        elif not data['category'] and not data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'])
        elif not data['category']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], brand_pubs=data['brand'])
        elif not data['brand']:
            entities = self.product_rep.filter_products(price_min=data['price__min'], price_max=data['price__max'], sort_by=data['sort_by'], category_pubs=data['category'])

        return self.create_product_dtos(entities)

    def _filter_products_by_slug_of_category(self, *args, **kwargs) -> list[ProductDTO]:
        return self.create_product_dtos(self.product_rep.filter_by_category_slug(category_slug=kwargs['category']))


    def post(self):
        """Whole workflow goes through get_context_data and get_queryset"""
        pass
    
class ProductPageService(BaseShopTemplateService):
    def __init__(
            self, 
            product_images_repository: IProductImagesRepository, 
            product_rating_repository: IProductRatingRepository, 
            review_repository: IReviewRepository, 
            review_read_model: IReviewReadModel, 
            **kwargs
        ):
        super().__init__(**kwargs)
        self.rating_rep = product_rating_repository
        self.review_rep = review_repository
        self.product_images_rep = product_images_repository
        self.review_read_model = review_read_model

    #@BaseCachingMixin.cache_result("get_object_{url_parameters}")
    def get_object(self, url_parameters: Any) -> ProductDTO:
        category_slug = url_parameters.get('category', None)
        product_slug = url_parameters.get('product', None)

        self.entity = self.product_rep.fetch_by_slugs(product_slug=product_slug, category_slug=category_slug, load_images=True, load_sizes=True)
        return ProductDTO.from_entity(
            self.entity,
            self.template_service.category_rep.fetch_by_uuid(self.entity.category.public_uuid),
            self.brand_rep.fetch_by_uuid(self.entity.brand.public_uuid),
            url_mapping_adapter=self.url_mapping,
        )

    def get_context_data(self, context: dict[str: Any], product_dto: ProductDTO) -> dict[str: Any]:
        header_and_footer = self.template_service.get_header_and_footer()
        product_rating = self.rating_rep.fetch_rating_by_product_uuid(self.entity.inner_uuid)
        product_rating_dto = ProductRatingDTO.from_entity(product_rating)
        
        context['product_images'] = self.entity.images
        context['related_products'] = self.product_rep.fetch_related_products(brand=self.entity.brand.inner_uuid, limit=10, select_related='category')
        context['product_rating'] = product_rating_dto
        context['stars'], context['reviews_count'] = self.review_read_model.fetch_rating_product_stars(product_rating.inner_uuid)

        # if self.is_authorized:
        #     context['add_to_cart'] = AddToCartForm(object_entity=ProductDTO.from_entity(entity), cart_pk=request.user.cart.pk)
        #     context['add_to_wishlist'] = AddToWishlistForm(object_entity=ProductDTO.from_entity(entity), wishlist_pk=request.user.wishlist.pk) 
 
        return {**header_and_footer, **context}

    def post(self, request: HttpRequest, object: Any) -> None:
        data = request.POST.copy()
        data['product'] = object.pk
        data['cart'] = request.user.cart.pk
        form = AddToCartForm(data, object=object, cart_pk=request.user.cart.pk)
        if form.is_valid():
            form.save() 

def store_search(query: str, category_public_uuid: str, session_adapter: RedisSessionHost):
    session_adapter.set({'search-query': query, 'search-category': category_public_uuid}, expire=30)
