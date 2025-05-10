from core.cart_management.domain.value_objects.cart_management import Size
from core.utils.application.base_dto import BaseDTO

from core.shop_management.application.dtos.shop_management import ProductSizeDTO, ProductImageDTO, ProductDTO as ExternalProductDTO
from core.user_management.application.dtos.user_management import UserDTO

from pydantic import Field, model_validator, field_validator
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
    color: list[str] | None = Field(default=None, title="Product Color", description="The color field must contain a list of strings that represent avaliable colors")
    sizes: list[SizeDTO] | None = Field(default=None, title="Product Sizes")
    images: list[str] | None = Field(default=None, title="Product Images")

    @field_validator("images", mode="before")
    @classmethod
    def validate_images(cls, value):
        if isinstance(value, list) and all(isinstance(i, ProductImageDTO) for i in value):
            return [str(i) for i in value]
        return value

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
            images = product.images if product.images else None, #pyright: ignore[reportArgumentType]
        )

class ACLUserDTO(BaseDTO["ACLUserDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    username: str | None = Field(default=None, min_length=2, max_length=225, title="Username")
    email: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", min_length=2, max_length=100, title="Email")
    first_name: str | None = Field(default=None, min_length=2, max_length=225, title="First Name")
    last_name: str | None = Field(default=None, min_length=2, max_length=225, title="Last Name")
    role: str | None = Field(default=None, examples=["user", "guest", "admin"], title="Role")

    @model_validator(mode="before")
    def validate_pub_uuid(cls, values):
        role = values.get('role')
        if role == "guest":
            values['pub_uuid'] = None
        return values

    @classmethod
    def from_user_dto(cls, dto: UserDTO) -> 'ACLUserDTO':
        return cls(
            pub_uuid=dto.pub_uuid,
            username=dto.username,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            role=dto.role,
        )

    @property
    def is_authenticated(self) -> bool:
        return self.role != 'guest' and self.pub_uuid is not None
