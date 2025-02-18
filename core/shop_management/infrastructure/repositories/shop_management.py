from typing import Any, Optional
from datetime import timedelta
import uuid

from django.db.models import Manager, Prefetch
from django.utils import timezone
from django.http import Http404

from core.shop_management.presentation.shop_management.models import Category as CategoryModel, Brand as BrandModel, Product as ProductModel, ProductSizes as ProductSizesModel, MultipleProductImages as MultipleProductImagesModel
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import ForeignUUID
from core.exceptions import InvalidFilterTypeException
from core.utils.domain.custom_structures import ProductImagesEntityList, ProductSizesEntityList, has_select_related
from ...domain.interfaces.i_repositories.i_shop_management import *

class DjangoCategoryRepository(ICategoryRepository):
    @staticmethod
    def map_category_into_entity(model: CategoryModel) -> CategoryEntity:
        return CategoryEntity(
            name=model.name,
            slug=model.slug,
            count_of_deals=model.count_of_deals,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )
    
    def fetch_categories(self, limit: Optional[int]=None, order: Optional[str]=None) -> list[CategoryEntity]:
        queryset = CategoryModel.objects.all()

        if order:
            queryset = queryset.order_by(order)

        if limit:
            queryset = queryset[:limit]

        return [self.map_category_into_entity(model) for model in queryset]

    def fetch_category_by_slug(self, slug: str) -> Optional[CategoryEntity]:
        try:
            return self.map_category_into_entity(CategoryModel.objects.get(slug=slug))
        except CategoryModel.DoesNotExist:
            return None
        
    def fetch_categories_by_uuids(self, uuids: list[str]) -> list[CategoryEntity]:
        categories = CategoryModel.objects.filter(public_uuid__in=uuids)
        return [self.map_category_into_entity(model) for model in categories]
    
    @staticmethod
    def fetch_categories_for_form(limit: int = 1) -> list[CategoryEntity]:
        categories = CategoryModel.objects.all()[:limit]
        return [DjangoCategoryRepository.map_category_into_entity(model) for model in categories]
    

    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> CategoryEntity:
        return self.map_category_into_entity(CategoryModel.objects.get(public_uuid=pub_uuid))



class DjangoBrandRepository(IBrandRepository):
    @staticmethod
    def map_brand_into_entity(model: BrandModel) -> BrandEntity:
        return BrandEntity(
            name=model.name,
            slug=model.slug,
            count_of_deals=model.count_of_deals,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )

    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> BrandEntity:
        return self.map_brand_into_entity(BrandModel.objects.get(public_uuid=pub_uuid))

    def fetch_brands(self, limit: Optional[int] = 0) -> list[BrandEntity]:        
        queryset = BrandModel.objects.all()[:limit] if limit else BrandModel.objects.all()
        return [self.map_brand_into_entity(model) for model in queryset]

    @staticmethod
    def fetch_brands_for_form(limit: Optional[int] = 1) -> list[BrandEntity]:        
        queryset = BrandModel.objects.all()[:limit]
        return [DjangoBrandRepository.map_brand_into_entity(model) for model in queryset]

    

class DjangoProductSizesRepository(IProductSizesRepository):
    @staticmethod
    def map_size_into_entity(model: ProductSizesModel, product_model: Optional[ProductModel] = None) -> ProductSizeEntity:
        product_model = model.product if not product_model else product_model
        return ProductSizeEntity(
            size=model.size,
            length=model.length,
            width=model.width,
            height=model.height,
            weight=model.weight,
            product=ForeignUUID(product_model.inner_uuid, product_model.public_uuid)
        )
    
    @staticmethod
    def map_sizes_into_entities(queryset: Manager[ProductSizesModel]) -> ProductSizesEntityList[ProductSizeEntity]:
        queryset = queryset.select_related('product')
        return ProductSizesEntityList(DjangoProductSizesRepository.map_size_into_entity(entity) for entity in queryset)
    
    def get_sizes_by_product_uuid(self, product_inner_uuid: Union[ForeignUUID, uuid.UUID]) -> ProductSizesEntityList[ProductSizeEntity]:
        product_inner_uuid = product_inner_uuid if isinstance(product_inner_uuid, uuid.UUID) else product_inner_uuid.inner_uuid
        return self.map_sizes_to_entities(ProductSizesModel.objects.filter(product__inner_uuid=product_inner_uuid))

    
class DjangoProductImagesRepository(IProductImagesRepository):
    @staticmethod
    def map_image_into_entity(model: MultipleProductImagesModel, product_model: Optional[ProductModel] = None) -> ProductImageEntity:
        product_model = model.product if not product_model else product_model
        return ProductImageEntity(
            image=model.image.url,
            product=ForeignUUID(product_model.inner_uuid, product_model.public_uuid)
        )
    
    @staticmethod
    def map_images_into_entities(queryset: Manager[MultipleProductImagesModel]) -> ProductImagesEntityList[ProductImageEntity]:
        if not has_select_related(queryset, 'product'):
            queryset = queryset.select_related('product')
        return ProductImagesEntityList(DjangoProductImagesRepository.map_image_into_entity(entity) for entity in queryset)
    
    def get_images_by_product_uuid(self, product_inner_uuid: Union[ForeignUUID, uuid.UUID]) -> ProductImagesEntityList[ProductImageEntity]:
        product_inner_uuid = product_inner_uuid if isinstance(product_inner_uuid, uuid.UUID) else product_inner_uuid.inner_uuid
        return self.map_images_into_entities(MultipleProductImagesModel.objects.filter(product__inner_uuid=product_inner_uuid))


class DjangoProductRepository(IProductRepository):
    @staticmethod
    def map_product_into_entity(
            model: ProductModel,
            load_sizes: bool = False,
            load_images: bool = False,
        ) -> ProductEntity:
        
        brand = model.brand
        category = model.category

        sizes = None
        if load_sizes:
            sizes = DjangoProductSizesRepository.map_sizes_into_entities(queryset=model.product_sizes.all())

        images = None
        if load_images:
            images = DjangoProductImagesRepository.map_images_into_entities(queryset=model.product_images.all())

        return ProductEntity(
            name=model.name,
            slug=model.slug,
            description=model.description,
            details=model.details,
            image=model.image.url,
            price=model.price,
            discount=model.discount,
            color=model.color,
            in_stock=model.in_stock,
            count_of_selled=model.count_of_selled,
            time_created=model.time_created,
            time_updated=model.time_updated,
            brand=ForeignUUID(brand.inner_uuid, brand.public_uuid),
            category=ForeignUUID(category.inner_uuid, category.public_uuid),
            #seller=model.seller.inner_uuid,
            seller=None,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
            sizes=sizes,
            images=images,
        )
    
    def fetch_product_by_uuid(
            self,
            inner_uuid: uuid.UUID | None,
            public_uuid: uuid.UUID | None,
            load_sizes: bool | None = None,
            load_images: bool | None = None,
        ) -> ProductEntity:

        if inner_uuid:
            product_model = ProductModel.objects.get(inner_uuid=inner_uuid)
        elif public_uuid:
            product_model = ProductModel.objects.get(public_uuid=public_uuid)
        else:
            return ProductEntity(inner_uuid=None, public_uuid=None)

        return self.map_product_into_entity(product_model, load_sizes=load_sizes, load_images=load_images)
    
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

        return [self.map_product_into_entity(model) for model in queryset]


    def searching_products(self, name: str | None = None, category_inner: uuid.UUID | None = None) -> list[ProductEntity]:
        queryset = ProductModel.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if category_inner:
            queryset = queryset.filter(category__inner_uuid=category_inner)

        return [self.map_product_into_entity(model) for model in queryset]
    

    def fetch_hot_deals(self, days: int) -> list[ProductEntity]:
        hot_week = timezone.now() - timedelta(days=days)
        queryset = ProductModel.objects.filter(time_created__gte=hot_week)
        return [self.map_product_into_entity(model) for model in queryset]

    def filter_by_category_slug(self, category_slug: str) -> list[ProductEntity]:
        queryset = ProductModel.objects.filter(category__slug=category_slug)
        return [self.map_product_into_entity(model) for model in queryset]
    
    def fetch_by_slugs(self, category_slug: str, product_slug: str, load_sizes: bool, load_images: bool) -> ProductEntity:
        try:
            model = ProductModel.objects.get(slug=product_slug, category__slug=category_slug)
        except model.model.DoesNotExist:
            raise Http404("No product found matching the query")
        return self.map_product_into_entity(model, load_sizes=load_sizes, load_images=load_images)

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

        return queryset

    def fetch_top_selling(self, amount: int, indent: int = 0) -> list[ProductEntity]:
        queryset = ProductModel.objects.select_related('category').prefetch_related(
            Prefetch('product_sizes', queryset=ProductSizesModel.objects.all().distinct())
        )
        
        if amount:
            queryset = queryset.distinct()[indent:amount]
        else:
            queryset = queryset.distinct()

        return [self.map_product_into_entity(model) for model in queryset]