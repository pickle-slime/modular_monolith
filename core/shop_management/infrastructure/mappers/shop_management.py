from django.db.models import QuerySet

from core.shop_management.presentation.shop_management.models import Category as CategoryModel, Brand as BrandModel, Product as ProductModel, ProductSizes as ProductSizesModel, MultipleProductImages as MultipleProductImagesModel
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import ForeignUUID
from core.shop_management.domain.structures import ProductImagesEntityList, ProductSizesEntityList


class DjangoCategoryMapper:
    @staticmethod
    def map_category_into_entity(model: CategoryModel) -> CategoryEntity:
        return CategoryEntity(
            name=model.name,
            slug=model.slug,
            count_of_deals=model.count_of_deals,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )
    
class DjangoBrandMapper:
    @staticmethod
    def map_brand_into_entity(model: BrandModel) -> BrandEntity:
        return BrandEntity(
            name=model.name,
            slug=model.slug,
            count_of_deals=model.count_of_deals,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )
    

class DjangoProductSizesMapper:
    @staticmethod
    def map_size_into_entity(model: ProductSizesModel, product_model: ProductModel | None = None) -> ProductSizeEntity:
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
    def map_sizes_into_entities(queryset: QuerySet[ProductSizesModel]) -> ProductSizesEntityList[ProductSizeEntity]:
        return ProductSizesEntityList(
            DjangoProductSizesMapper.map_size_into_entity(entity) 
            for entity in queryset.select_related("product")
        )
    
class DjangoProductImagesMapper:
    @staticmethod
    def map_image_into_entity(model: MultipleProductImagesModel, product_model: ProductModel | None = None) -> ProductImageEntity:
        product_model = model.product if not product_model else product_model
        return ProductImageEntity(
            image=model.image.url,
            product=ForeignUUID(product_model.inner_uuid, product_model.public_uuid)
        )
    
    @staticmethod
    def map_images_into_entities(queryset: QuerySet[MultipleProductImagesModel]) -> ProductImagesEntityList[ProductImageEntity]:
        return ProductImagesEntityList(
            DjangoProductImagesMapper.map_image_into_entity(entity) 
            for entity in queryset.select_related("product")
        )
    
class DjangoProductMapper:
    @staticmethod
    def map_product_into_entity(
        model: ProductModel,
        sizes_queryset: ProductSizesModel | QuerySet[ProductSizesModel] | None = None,
        images_queryset: MultipleProductImagesModel | QuerySet[MultipleProductImagesModel] | None = None,
    ) -> ProductEntity:

        sizes = DjangoProductMapper._map_sizes(sizes_queryset)
        images = DjangoProductMapper._map_images(images_queryset)
        
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
            brand=ForeignUUID(model.brand.inner_uuid, model.brand.public_uuid),
            category=ForeignUUID(model.category.inner_uuid, model.category.public_uuid),
            seller=model.seller.public_uuid,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
            sizes=sizes,
            images=images,
        )
    
    @staticmethod
    def _map_sizes(sizes_queryset: ProductSizesModel | QuerySet[ProductSizesModel] | None) -> ProductSizesEntityList | ProductSizeEntity | None:
        """Handles mapping of size sub-entities."""
        if sizes_queryset is None:
            return None
        if isinstance(sizes_queryset, ProductSizesModel):
            return DjangoProductSizesMapper.map_size_into_entity(sizes_queryset)
        return ProductSizesEntityList(DjangoProductSizesMapper.map_sizes_into_entities(sizes_queryset))

    @staticmethod
    def _map_images(images_queryset: MultipleProductImagesModel | QuerySet[MultipleProductImagesModel] | None) -> ProductImagesEntityList | ProductImageEntity | None:
        """Handles mapping of image sub-entities."""
        if images_queryset is None:
            return None
        if isinstance(images_queryset, MultipleProductImagesModel):
            return DjangoProductImagesMapper.map_image_into_entity(images_queryset)
        return ProductImagesEntityList(DjangoProductImagesMapper.map_images_into_entities(images_queryset))
