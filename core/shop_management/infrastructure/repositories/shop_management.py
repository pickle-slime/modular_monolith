from typing import Optional
from datetime import timedelta
import uuid

from django.db.models import Prefetch
from django.db import transaction, connection
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator


from core.shop_management.application.dtos.infrastructure import PaginatedProductsInfDTO
from core.shop_management.presentation.shop_management.models import Category as CategoryModel, Brand as BrandModel, Product as ProductModel, ProductSizes as ProductSizesModel, MultipleProductImages as MultipleProductImagesModel
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.shop_management.domain.interfaces.i_repositories.i_shop_management import *
from core.shop_management.application.interfaces.i_read_models.i_shop_management import IProductReadModel
from core.shop_management.application.exceptions import ProductNotFoundError, SizeNotFoundError

from core.shop_management.application.dtos.acl_dtos import ACLWishlistItemDTO, ACLCartItemDTO
from core.shop_management.application.dtos.composition import WishlistItemDetailsDTO, CartItemDetailsDTO

from ..mappers.shop_management import DjangoCategoryMapper, DjangoBrandMapper, DjangoProductMapper

class DjangoCategoryRepository(ICategoryRepository):
    def fetch_categories(self, limit: Optional[int]=None, order: Optional[str]=None) -> list[CategoryEntity]:
        queryset = CategoryModel.objects.all()

        if order:
            queryset = queryset.order_by(order)

        if limit:
            queryset = queryset[:limit]

        return [DjangoCategoryMapper.map_category_into_entity(model) for model in queryset]

    def fetch_category_by_slug(self, slug: str) -> Optional[CategoryEntity]:
        try:
            return DjangoCategoryMapper.map_category_into_entity(CategoryModel.objects.get(slug=slug))
        except CategoryModel.DoesNotExist:
            return None
        
    def fetch_categories_by_uuids(self, uuids: list[str]) -> list[CategoryEntity]:
        categories = CategoryModel.objects.filter(public_uuid__in=uuids)
        return [DjangoCategoryMapper.map_category_into_entity(model) for model in categories]
    
    @staticmethod
    def fetch_categories_for_form(limit: int = 1) -> list[CategoryEntity]:
        categories = CategoryModel.objects.all()[:limit]
        return [DjangoCategoryMapper.map_category_into_entity(model) for model in categories]
    

    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> CategoryEntity:
        return DjangoCategoryMapper.map_category_into_entity(CategoryModel.objects.get(public_uuid=pub_uuid))



class DjangoBrandRepository(IBrandRepository):
    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> BrandEntity:
        return DjangoBrandMapper.map_brand_into_entity(BrandModel.objects.get(public_uuid=pub_uuid))

    def fetch_brands(self, limit: Optional[int] = 0) -> list[BrandEntity]:        
        queryset = BrandModel.objects.all()[:limit] if limit else BrandModel.objects.all()
        return [DjangoBrandMapper.map_brand_into_entity(model) for model in queryset]

    @staticmethod
    def fetch_brands_for_form(limit: Optional[int] = 1) -> list[BrandEntity]:        
        queryset = BrandModel.objects.all()[:limit]
        return [DjangoBrandMapper.map_brand_into_entity(model) for model in queryset]


class DjangoProductRepository(IProductRepository):
    def fetch_product_by_uuid(
            self,
            inner_uuid: uuid.UUID | None,
            public_uuid: uuid.UUID | None,
        ) -> ProductEntity:

        if inner_uuid:
            product_model = ProductModel.objects.get(inner_uuid=inner_uuid)
        elif public_uuid:
            product_model = ProductModel.objects.get(public_uuid=public_uuid)
        else:
            raise ValueError(f"{self.__class__.__name__}.{self.fetch_product_by_uuid.__name__}: must have at least inner_uuid or public_uuid")

        return DjangoProductMapper.map_product_into_entity(product_model)

    def all(self) -> list[ProductEntity]:
        return [DjangoProductMapper.map_product_into_entity(model) for model in ProductModel.objects.all()]
    
    def filter_products(
        self,
        price_min: float,
        price_max: float,
        sort_by: Literal['count_of_selled', 'price', '-time_updated'],
        page: int,
        per_page: int,
        category_pubs: list[uuid.UUID] | None = None,
        brand_pubs: list[uuid.UUID] | None = None,
    ) -> PaginatedProductsInfDTO:
        queryset = ProductModel.objects.all().order_by((sort_by if isinstance(sort_by, str) else "inner_uuid"))
        queryset = queryset.filter(price__gt=price_min, price__lt=price_max).order_by(sort_by)

        if category_pubs:
            queryset = queryset.filter(category__public_uuid__in=category_pubs)
        if brand_pubs:
            queryset = queryset.filter(brand__public_uuid__in=brand_pubs)
            
        queryset = queryset.select_related('category', 'brand')

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return DjangoProductMapper.map_entities_to_paginated_dto(page_obj) 

    def searching_products(self, page: int, per_page: int, query: str | None = None, category_pub: uuid.UUID | None = None) -> PaginatedProductsInfDTO:
        queryset = ProductModel.objects.all()

        if query:
            queryset = queryset.filter(name__icontains=query)
        
        if category_pub:
            queryset = queryset.filter(category__public_uuid=category_pub)

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return DjangoProductMapper.map_entities_to_paginated_dto(page_obj)
    

    def fetch_hot_deals(self, days: int) -> list[ProductEntity]:
        hot_week = timezone.now() - timedelta(days=days)
        queryset = ProductModel.objects.filter(time_created__gte=hot_week)
        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]

    def filter_by_category_slug(self, page: int, per_page: int, category_slug: str | None) -> PaginatedProductsInfDTO:
        if category_slug:
            queryset = ProductModel.objects.filter(category__slug=category_slug)
        else:
            queryset = ProductModel.objects.all()

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return DjangoProductMapper.map_entities_to_paginated_dto(page_obj)
    
    def fetch_by_slugs(self, category_slug: str, product_slug: str) -> ProductEntity:
        try:
            model = ProductModel.objects.get(slug=product_slug, category__slug=category_slug)
            sizes = ProductSizesModel.objects.filter(product__inner_uuid=model.inner_uuid)
            images = MultipleProductImagesModel.objects.filter(product__inner_uuid=model.inner_uuid)
        except (ProductModel.DoesNotExist, ProductSizesModel.DoesNotExist, MultipleProductImagesModel.DoesNotExist):
            raise Http404("No product found matching the query")
        return DjangoProductMapper.map_product_into_entity(model, sizes, images)

    def fetch_related_products(
            self,
            brand: uuid.UUID,
            limit: int = 1,
            select_related: Optional[str] = None
        ) -> list[ProductEntity]:
        """
        Fetch products with filters, optional select_related and limit.
        """
        queryset = ProductModel.objects.filter(brand__inner_uuid=brand)[:limit]

        if isinstance(select_related, str):
            queryset = queryset.select_related(select_related)

        return [DjangoProductMapper.map_product_into_entity(product) for product in queryset]

    def fetch_top_selling(self, amount: int, indent: int = 0) -> list[ProductEntity]:
        queryset = ProductModel.objects.select_related('category').prefetch_related(
            Prefetch('product_sizes', queryset=ProductSizesModel.objects.all().distinct())
        )
        
        if amount:
            queryset = queryset.distinct()[indent:amount]
        else:
            queryset = queryset.distinct()

        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]

    def fetch_paginated_top_selling(self, page: int, per_page: int) -> PaginatedProductsInfDTO:
        queryset = ProductModel.objects.select_related('category').prefetch_related(
            Prefetch('product_sizes', queryset=ProductSizesModel.objects.all().distinct())
        )
       
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return DjangoProductMapper.map_entities_to_paginated_dto(page_obj)
    
    def fetch_sample_of_size(
        self,
        public_uuid: uuid.UUID,
        size_public_uuid: uuid.UUID | None,
    ) -> ProductEntity:
        '''Fetches the product by public uuid with size by size's public uuid, the image is first one'''

        try:
            product = ProductModel.objects.get(public_uuid=public_uuid)
        except ProductModel.DoesNotExist:
            raise ProductNotFoundError(f"Can't find product by uuid ({public_uuid})")

        try:
            if size_public_uuid:
                size = ProductSizesModel.objects.get(public_uuid=size_public_uuid)
            else:
                size = ProductSizesModel.objects.filter(product__public_uuid=public_uuid)[0]
        except ProductSizesModel.DoesNotExist:
            raise SizeNotFoundError(f"Can't find size by uuid ({size_public_uuid})")

        return DjangoProductMapper.map_product_into_entity(product, sizes_queryset=size)

class ProductReadModel(IProductReadModel):
    @transaction.atomic()
    def fetch_wishlist_items_details(self, items: list[ACLWishlistItemDTO]) -> list[WishlistItemDetailsDTO]:
        public_uuids = [i.size for i in items]  

        if not public_uuids:
            return []

        sql = '''
            SELECT s.public_uuid, p.public_uuid, p.name, p.image, p.price, p.discount, c.slug, p.slug 
            FROM shop_management_product p
            INNER JOIN shop_management_productsizes s ON p.inner_uuid = s.product_id
            INNER JOIN shop_management_category c ON c.inner_uuid = p.category_id
            WHERE s.public_uuid = ANY(%s);
        '''

        with connection.cursor() as cursor:
            cursor.execute(sql, [[public_uuids]])
            rows: list[tuple] = cursor.fetchall()

        return [WishlistItemDetailsDTO(
            size=row[0], 
            product_pub_uuid=row[1],
            product_name=row[2], 
            image=row[3], 
            price=row[4], 
            discount=row[5], 
            category_slug=row[6], 
            product_slug=row[7]) 
                for row in rows]

    @transaction.atomic()
    def fetch_cart_items_details(self, items: list[ACLCartItemDTO]) -> list[CartItemDetailsDTO]:
        public_uuids = [i.size for i in items]  

        if not public_uuids:
            return []

        sql = '''
            SELECT s.public_uuid, p.public_uuid, p.name, p.image, p.price, p.discount, c.slug, p.slug 
            FROM shop_management_product p
            INNER JOIN shop_management_productsizes s ON p.inner_uuid = s.product_id
            INNER JOIN shop_management_category c ON c.inner_uuid = p.category_id
            WHERE s.public_uuid = ANY(%s);
        '''

        with connection.cursor() as cursor:
            cursor.execute(sql, [[public_uuids]])
            rows: list[tuple] = cursor.fetchall()

        return [CartItemDetailsDTO(
            size=row[0], 
            product_pub_uuid=row[1],
            product_name=row[2], 
            image=row[3], 
            price=row[4], 
            discount=row[5], 
            category_slug=row[6], 
            product_slug=row[7]) 
                for row in rows]
