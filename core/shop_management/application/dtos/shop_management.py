from pydantic import field_validator, Field
from typing import Iterable, Optional
from datetime import datetime
from decimal import Decimal
import uuid

from core.utils.application.base_dto import BaseEntityDTO, BaseDTO
from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductImage as ProductImageEntity, ProductSize as ProductSizeEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import CommonNameField, CommonSlugField
from core.shop_management.domain.value_objects.shop_management import ImageField, PercentageField
from core.shop_management.domain.structures import ProductImagesEntityList, ProductSizesEntityList
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

class CategoryDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=5, max_length=100, title="Category Name")
    slug: str | None = Field(default=None, min_length=5, max_length=100, title="Category Name")
    count_of_deals: int | None = Field(default=None, ge=0, title="Count of Deals") 

    get_absolute_url: str | None = Field(default=None, title="Absolute Url", description="Contains a path to the dedicated web page")

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
    def from_entity(cls: type["CategoryDTO"], entity: CategoryEntity, url_mapping_adapter: Optional[URLHost] = None) -> "CategoryDTO":
        absolute_url = url_mapping_adapter.get_absolute_url_of_category(entity.slug) if url_mapping_adapter and isinstance(entity, CategoryEntity) else None
        return cls(
            pub_uuid=entity.public_uuid,
            name=entity.name,
            slug=entity.slug,
            count_of_deals=entity.count_of_deals,
            get_absolute_url=absolute_url
        )

class BrandDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=2, max_length=100, title="Brand Name")
    slug: str | None = Field(default=None, min_length=2, max_length=100, title="Brand Name")
    count_of_deals: int | None = Field(default=None, ge=0, title="Count of Deals", alias="countOfDeals")

    get_absolute_url: str | None = Field(default=None, title="Absolute Url", description="Contains a path to the dedicated web page", alias="absoluteUrl")

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
    def from_entity(cls: type['BrandDTO'], entity: BrandEntity, url_mapping_adapter: Optional[URLHost] = None) -> 'BrandDTO':
        absolute_url = url_mapping_adapter.get_absolute_url_of_brand(entity.slug) if url_mapping_adapter and isinstance(entity, BrandEntity) else None
        return cls(
            pub_uuid=entity.public_uuid,
            name=entity.name,
            slug=entity.slug,
            count_of_deals=entity.count_of_deals,
            get_absolute_url=absolute_url
        )
    
    @classmethod
    def from_entities(cls: type['BrandDTO'], entities: list[BrandEntity]) -> list['BrandDTO']:
        return [cls.from_entity(entity).populate_none_fields() for entity in entities]
    
    class Config:
        from_attributes = True

class ProductSizeDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)
    size: str | None = Field(default=None)
    
    length: Decimal | None = Field(default=None, title="Length")
    width: Decimal | None = Field(default=None, title="Width")
    height: Decimal | None = Field(default=None, title="Height")
    weight: Decimal | None = Field(default=None, title="Weight")

    product: uuid.UUID | None = Field(default=None, title="Product", description="Contatins the public uuid of an internal module")

    @classmethod
    def from_entity(cls: type['ProductSizeDTO'], entity: ProductSizeEntity) -> 'ProductSizeDTO':
        return cls(
            pub_uuid=entity.public_uuid,
            size=entity.size,
            length=entity.length,
            width=entity.weight,
            height=entity.height,
            weight=entity.weight,
            product=entity.product.public_uuid
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductSizeEntity] | ProductSizesEntityList[ProductSizeEntity]) -> list['ProductSizeDTO']:
        return [cls.from_entity(entity).populate_none_fields() for entity in entities]
    
    class Config:
        from_attributes = True


class ProductImageDTO(BaseEntityDTO):
    pub_uuid: uuid.UUID | None = Field(default=None)

    image: str | None = Field(default=None, title="Image")
    product: uuid.UUID | None = Field(default=None, title="Product", description="Contatins the public uuid of an internal module")

    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if isinstance(v, ImageField):
            return str(v)
        return v 

    @classmethod
    def from_entity(cls: type['ProductImageDTO'], entity: ProductImageEntity) -> 'ProductImageDTO':
        return cls(
            pub_uuid=entity.public_uuid,
            image=entity.image,
            product=entity.product.public_uuid
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductImageEntity] | ProductImagesEntityList[ProductImageEntity]) -> list['ProductImageDTO']:
        return [cls.from_entity(entity).populate_none_fields() for entity in entities]

    def __str__(self):
        return self.image

class ProductDTO(BaseEntityDTO['ProductDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None)

    name: str | None = Field(default=None, min_length=2, max_length=100, title="Product Name")
    slug: str | None = Field(default=None, min_length=2, max_length=100, title="Product Name")
    description: str | None = Field(default=None, title="Description")
    details: str | None = Field(default=None, title="Details")
    image: str | None = Field(default=None, title="Product Image URL", description="The field keeps the path of the image")
    price: float | None = Field(default=None, ge=0, title="Product Price")
    discount: int | None = Field(default=None, ge=0, le=100, title="Product Discout", description="The discount must be a percentage (0-100%)")
    color: list[str] | None = Field(default=None, title="Product Color", description="The color field must contain a list of strings that represent avaliable colors")
    in_stock: int | None = Field(default=None, ge=0, title="In Stock", alias="inStock")
    count_of_selled: int | None = Field(default=None, ge=0, title="Count of Sealed", alias="countOfSealed")
    time_created: datetime | None = Field(default=None, title="Time Created", alias="timeCreated")
    time_updated: datetime | None = Field(default=None, title="Time Updated", alias="timeUpdated")

    brand: BrandDTO | None = Field(default=None)
    category: CategoryDTO | None = Field(default=None)
    seller: uuid.UUID | None = Field(default=None, title="Product Seller", description="Contatins the public uuid of an external module")
    sizes: list[ProductSizeDTO] | None = Field(default=None, title="Product Sizes")
    images: list[ProductImageDTO] | None = Field(default=None, title="Product Images")

    get_absolute_url: str | None = Field(default=None, title="Absolute Url", description="Contains a path to the dedicated web page", alias="absoluteUrl")

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
        cls: type['ProductDTO'],
        entity: ProductEntity,
        category: Optional[CategoryEntity] = None,
        brand: Optional[BrandEntity] = None,
        url_mapping_adapter: Optional[URLHost] = None,
    ) -> 'ProductDTO':
        absolute_url = url_mapping_adapter.get_absolute_url_of_product(category.slug, entity.slug) if url_mapping_adapter and isinstance(category, CategoryEntity) else None
        return cls(
            pub_uuid=entity.public_uuid,
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
            sizes=ProductSizeDTO.from_entities(entity.sizes) if isinstance(entity.sizes, Iterable) and len(entity.sizes) > 1 else [ProductSizeDTO.from_entity(entity.sizes[0])] if entity.sizes else None,
            images=ProductImageDTO.from_entities(entity.images) if isinstance(entity.images, Iterable) and len(entity.images) > 1 else [ProductSizeDTO.from_entity(entity.images[0])] if entity.images else None,
            get_absolute_url=absolute_url,
        )
    
    @classmethod
    def from_entities(cls, entities: list[ProductEntity]) -> list['ProductDTO']:
        return [cls.from_entity(entity).populate_none_fields() for entity in entities]
