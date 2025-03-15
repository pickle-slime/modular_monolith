from typing import Any, Optional
from datetime import timedelta
import uuid

from django.db.models import Prefetch
from django.utils import timezone
from django.http import Http404

from core.shop_management.presentation.shop_management.models import Category as CategoryModel, Brand as BrandModel, Product as ProductModel, ProductSizes as ProductSizesModel, MultipleProductImages as MultipleProductImagesModel
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from ...domain.interfaces.i_repositories.i_shop_management import *

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
            return ProductEntity(inner_uuid=None, public_uuid=None)

        return DjangoProductMapper.map_product_into_entity(product_model)
    
    def filter_products(
        self,
        price_min: float,
        price_max: float,
        sort_by: Literal['count_of_selled', 'price', '-time_updated'],
        category_pubs: list[uuid.UUID] | None = None,
        brand_pubs: list[uuid.UUID] | None = None,
    ) -> list[ProductEntity]:
        queryset = ProductModel.objects.all().order_by((sort_by if isinstance(sort_by, str) else "id"))
        queryset = queryset.filter(price__gt=price_min, price__lt=price_max).order_by(sort_by)

        if category_pubs:
            queryset = queryset.filter(category__public_uuid__in=category_pubs)
        if brand_pubs:
            queryset = queryset.filter(brand__public_uuid__in=brand_pubs)
            
        queryset = queryset.select_related('category', 'brand')

        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]


    def searching_products(self, name: str | None = None, category_inner: uuid.UUID | None = None) -> list[ProductEntity]:
        queryset = ProductModel.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if category_inner:
            queryset = queryset.filter(category__inner_uuid=category_inner)

        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]
    

    def fetch_hot_deals(self, days: int) -> list[ProductEntity]:
        hot_week = timezone.now() - timedelta(days=days)
        queryset = ProductModel.objects.filter(time_created__gte=hot_week)
        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]

    def filter_by_category_slug(self, category_slug: str) -> list[ProductEntity]:
        queryset = ProductModel.objects.filter(category__slug=category_slug)
        return [DjangoProductMapper.map_product_into_entity(model) for model in queryset]
    
    def fetch_by_slugs(self, category_slug: str, product_slug: str) -> ProductEntity:
        try:
            model = ProductModel.objects.get(slug=product_slug, category__slug=category_slug)
            sizes = ProductSizesModel.objects.filter(product__inner_uuid=model.inner_uuid)
            images = MultipleProductImagesModel.objects.filter(product__inner_uuid=model.inner_uuid)
        except (model.model.DoesNotExist, sizes.model.DoesNotExist, images.model.DoesNotExist):
            raise Http404("No product found matching the query")
        return DjangoProductMapper.map_product_into_entity(model, sizes, images)

    def fetch_related_products(
            self,
            brand: str,
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
    
    def fetch_sample_of_size(
        self,
        public_uuid: uuid.UUID | None,
        size_public_uuid: uuid.UUID | None,
    ) -> ProductEntity:
        '''Fetches the product by public uuid with size by size's public uuid, the image is first one'''

        try:
            product = ProductModel.objects.get(public_uuid=public_uuid)
            size = ProductSizesModel.objects.get(public_uuid=size_public_uuid)
        except (ProductModel.DoesNotExist, ProductSizesModel.DoesNotExist):
            return ProductEntity(inner_uuid=None, public_uuid=None)

        return DjangoProductMapper.map_product_into_entity(product, sizes_queryset=size)