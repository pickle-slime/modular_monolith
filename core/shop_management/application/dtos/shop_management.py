from pydantic import field_validator
from typing import Type, Optional, Generic
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from core.utils.application.base_dto import BaseDTO
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductImage as ProductImageEntity, ProductSize as ProductSizeEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import CommonNameField, CommonSlugField
from core.shop_management.domain.value_objects.shop_management import ImageField, PercentageField, ProductSizesCollection, ProductImagesCollection
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

class CategoryDTO(BaseDTO):
    uuid: UUID
    name: str
    slug: str
    count_of_deals: int

    get_absolute_url: str | None = None

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, CommonNameField):
            return str(v)  
        return v  
    
    @field_validator("slug", mode="before")
    def validate_slug(cls, v):
        if isinstance(v, CommonSlugField):
            return str(v)
        return v  

    @classmethod
    def from_entity(cls: Type["CategoryDTO"], entity: CategoryEntity, url_mapping_adapter: Optional[URLHost] = None) -> "CategoryDTO":
        absolute_url = url_mapping_adapter.get_absolute_url_of_category(entity.slug) if url_mapping_adapter and isinstance(entity, CategoryEntity) else None
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            name=entity.name,
            slug=entity.slug,
            count_of_deals=entity.count_of_deals,
            get_absolute_url=absolute_url
        )

    class Config:
        from_attributes = True

class BrandDTO(BaseDTO):
    uuid: UUID
    name: str
    slug: str
    count_of_deals: int

    get_absolute_url: str | None = None

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, CommonNameField):
            return str(v)  
        return v  

    @field_validator("slug", mode="before")
    def validate_slug(cls, v):
        if isinstance(v, CommonSlugField):
            return str(v)
        return v  

    @classmethod
    def from_entity(cls: Type['BrandDTO'], entity: BrandEntity, url_mapping_adapter: Optional[URLHost] = None) -> 'BrandDTO':
        absolute_url = url_mapping_adapter.get_absolute_url_of_brand(entity.slug) if url_mapping_adapter and isinstance(entity, BrandEntity) else None
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            name=entity.name,
            slug=entity.slug,
            count_of_deals=entity.count_of_deals,
            get_absolute_url=absolute_url
        )
    
    @classmethod
    def from_entities(cls: Type['BrandDTO'], entities: list[BrandEntity]) -> list['BrandDTO']:
        return [cls.from_entity(entity) for entity in entities]
    
    class Config:
        from_attributes = True

class ProductSizeDTO(BaseDTO):
    size: str
    length: Decimal
    width: Decimal
    height: Decimal
    weight: Decimal

    entity: UUID

    uuid: UUID

    @classmethod
    def from_entity(cls: type['ProductSizeDTO'], entity: ProductSizeEntity, url_mapping_adapter: Optional[URLHost] = None) -> 'ProductSizeDTO':
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            size=entity.size,
            length=entity.length,
            width=entity.weight,
            height=entity.height,
            weight=entity.weight,
            entity=entity.product.public_uuid
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductSizeEntity] | ProductSizesCollection[ProductSizeEntity]) -> list['ProductSizeDTO']:
        return [cls.from_entity(entity) for entity in entities]
    
    class Config:
        from_attributes = True


class ProductImageDTO(BaseDTO):
    image: str
    entity: UUID
    uuid: UUID

    @classmethod
    def from_entity(cls: type['ProductImageDTO'], entity: ProductImageEntity, url_mapping_adapter: Optional[URLHost] = None) -> 'ProductImageDTO':
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            image=entity.image,
            entity=entity.product.public_uuid
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductImageEntity] | ProductImagesCollection[ProductImageEntity]) -> list['ProductImageDTO']:
        return [cls.from_entity(entity) for entity in entities]
    
    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if isinstance(v, ImageField):
            return str(v)
        return v 
    
    class Config:
        from_attributes = True

class ProductDTO(BaseDTO):
    name: str
    slug: str
    description: str
    details: str
    image: str
    price: int
    discount: int
    color: list[str]
    in_stock: int
    count_of_selled: int
    time_created: datetime
    time_updated: datetime

    brand: Optional[BrandDTO] = None
    category: Optional[CategoryDTO] = None
    seller: None = None
    entity_sizes: Optional[list[ProductSizeDTO]] = None
    entity_images: Optional[list[ProductImageDTO]] = None

    uuid: UUID

    get_absolute_url: str | None = None

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        if isinstance(v, CommonNameField):
            return str(v)  
        return v  

    @field_validator("slug", mode="before")
    def validate_slug(cls, v):
        if isinstance(v, CommonSlugField):
            return str(v)
        return v  

    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if isinstance(v, ImageField):
            return str(v)
        return v 
    
    @field_validator("discount", mode="before")
    def validate_discount(cls, v):
        if isinstance(v, PercentageField):
            return int(v)
        return v  


    @classmethod
    def from_entity(
        cls: Type['ProductDTO'],
        entity: ProductEntity,
        category: Optional[CategoryEntity] = None,
        brand: Optional[BrandEntity] = None,
        url_mapping_adapter: Optional[URLHost] = None,
        user = None,
    ) -> 'ProductDTO':
        absolute_url = url_mapping_adapter.get_absolute_url_of_product(category.slug, entity.slug) if url_mapping_adapter and isinstance(category, CategoryEntity) else None
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            name=entity.name,
            slug=entity.slug,
            description=entity.description,
            details=entity.details,
            image=entity.image,
            price=entity.price,
            discount=entity.discount,
            color=entity.color,
            in_stock=entity.in_stock,
            count_of_selled=entity.count_of_selled,
            time_created=entity.time_created,
            time_updated=entity.time_updated,

            brand=BrandDTO.from_entity(brand, url_mapping_adapter) if brand else None,
            category=CategoryDTO.from_entity(category, url_mapping_adapter) if category else None,
            #seller=entity.seller.public_uuid,
            entity_sizes=ProductSizeDTO.from_entities(entity.sizes) if entity.sizes else None,
            entity_images=ProductImageDTO.from_entities(entity.images) if entity.images else None,

            get_absolute_url=absolute_url,
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductEntity]) -> list['ProductDTO']:
        return [cls.from_entity(entity) for entity in entities]

    
    class Config:
        from_attributes = True
