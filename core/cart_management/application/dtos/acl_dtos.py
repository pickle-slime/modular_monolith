from core.cart_management.domain.value_objects.cart_management import Size
from core.utils.application.base_dto import BaseDTO

from core.shop_management.application.dtos.shop_management import ProductSizeDTO, ProductDTO as ExternalProductDTO

from pydantic import Field
from decimal import Decimal
import uuid

class SizeDTO(BaseDTO['SizeDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None)
    length: Decimal | None = Field(default=None, title="Length")
    width: Decimal | None = Field(default=None, title="Width")
    height: Decimal | None = Field(default=None, title="Height")
    weight: Decimal | None = Field(default=None, title="Weight")

    @staticmethod
    def from_product_size(size: ProductSizeDTO) -> 'SizeDTO':
        '''maps the external dto'''
        return SizeDTO(
            pub_uuid=size.pub_uuid,
            length=size.length,
            width=size.width,
            height=size.height,
            weight=size.weight,
        )

    def to_size_vo(self) -> Size:
        return Size(**self.model_dump())
    
class ProductDTO(BaseDTO['ProductDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=5, max_length=100, title="Produt Name")
    slug: str | None = Field(default=None, min_length=5, max_length=100, title="Produt Slug")
    image: str | None = Field(default=None, title="Product Image URL", description="The field keeps the path of the image")
    price: float | None = Field(default=None, ge=0, title="Product Price")
    discount: int | None = Field(default=None, ge=0, le=100, title="Product Discout", description="The discount must be a percentage (0-100%)")
    color: str | None = Field(default=None, title="Product Color", description="The color field must contain a list of strings that represent avaliable colors")
    sizes: list[SizeDTO] | None = Field(default=None, title="Product Sizes")
    images: list[str] | None = Field(default=None, title="Product Images")

    @staticmethod
    def from_product(product: ExternalProductDTO) -> 'ProductDTO':
        return ProductDTO(
            pub_uuid=product.pub_uuid,
            name = product.name,
            slug = product.slug,
            image = product.image,
            price = product.price,
            discount = product.discount,
            color = product.color,
            sizes = [SizeDTO.from_product_size(i) for i in product.sizes] if product.sizes else None,
            images = list(product.images) if product.images else None,
        )
