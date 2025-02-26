from pydantic import field_validator, Field
from typing import Type, Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from core.utils.application.base_dto import BaseEntityDTO
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductImage as ProductImageEntity, ProductSize as ProductSizeEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import CommonNameField, CommonSlugField
from core.shop_management.domain.value_objects.shop_management import ImageField, PercentageField, ProductSizesCollection, ProductImagesCollection
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

class CategoryDTO(BaseEntityDTO):
    uuid: UUID | None = Field(default=None)
    name: str | None = Field(default=None)
    slug: str | None = Field(default=None) 
    count_of_deals: int = Field(default=0)

    get_absolute_url: str | None = Field(default=None)

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

class BrandDTO(BaseEntityDTO):
    uuid: UUID = Field(default=None)
    name: str | None = Field(default=None)
    slug: str | None = Field(default=None)
    count_of_deals: int = Field(default=0)

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

class ProductSizeDTO(BaseEntityDTO):
    size: str | None = Field(default=None)
    length: Decimal = Field(default=Decimal(0.0))
    width: Decimal = Field(default=Decimal(0.0))
    height: Decimal = Field(default=Decimal(0.0))
    weight: Decimal = Field(default=Decimal(0.0))

    product: UUID | None = Field(default=None)

    uuid: UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls: type['ProductSizeDTO'], entity: ProductSizeEntity) -> 'ProductSizeDTO':
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            size=entity.size,
            length=entity.length,
            width=entity.weight,
            height=entity.height,
            weight=entity.weight,
            product=entity.product.public_uuid
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductSizeEntity] | ProductSizesCollection[ProductSizeEntity]) -> list['ProductSizeDTO']:
        return [cls.from_entity(entity) for entity in entities]
    
    class Config:
        from_attributes = True


class ProductImageDTO(BaseEntityDTO):
    image: str | None = Field(default=None)
    product: UUID | None = Field(default=None)
    uuid: UUID | None = Field(default=None)

    @classmethod
    def from_entity(cls: type['ProductImageDTO'], entity: ProductImageEntity) -> 'ProductImageDTO':
        return cls(
            uuid=UUID(str(entity.public_uuid)) if not isinstance(entity.public_uuid, UUID) else entity.public_uuid,
            image=entity.image,
            product=entity.product.public_uuid
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

class ProductDTO(BaseEntityDTO):
    name: str | None = Field(default=None)
    slug: str | None = Field(default=None)
    description: str | None = Field(default=None)
    details: str | None = Field(default=None)
    image: str | None = Field(default=None)
    price: int = Field(default=0)
    discount: int = Field(default=0)
    color: list[str] | None = Field(default=None)
    in_stock: int = Field(default=0)
    count_of_selled: int = Field(default=0)
    time_created: datetime | None = Field(default=None)
    time_updated: datetime | None = Field(default=None)

    brand: BrandDTO | None = Field(default=None)
    category: CategoryDTO | None = Field(default=None)
    seller: UUID | None = Field(default=None)
    entity_sizes: list[ProductSizeDTO] | None = Field(default=None)
    entity_images: list[ProductImageDTO] | None = Field(default=None)

    uuid: UUID | None = Field(default=None)

    get_absolute_url: str = Field(default="/")

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

    @field_validator("get_absolute_url", mode="before")
    def validate_get_absolute_url(cls, v):
        return v if v is not None else "/"

    @classmethod
    def from_entity(
        cls: Type['ProductDTO'],
        entity: ProductEntity,
        category: Optional[CategoryEntity] = None,
        brand: Optional[BrandEntity] = None,
        url_mapping_adapter: Optional[URLHost] = None,
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
            seller=entity.seller,
            entity_sizes=ProductSizeDTO.from_entities(entity.sizes) if entity.sizes else None,
            entity_images=ProductImageDTO.from_entities(entity.images) if entity.images else None,

            get_absolute_url=absolute_url,
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductEntity]) -> list['ProductDTO']:
        return [cls.from_entity(entity) for entity in entities]

    
    class Config:
        from_attributes = True
