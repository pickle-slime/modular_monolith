from core.shop_management.application.dtos.base_dto import BaseDTO

from pydantic import Field
import uuid

class WishlistItemDetailsDTO(BaseDTO["WishlistItemDetailsDTO"]):
    size: uuid.UUID = Field(title="Size", description="Represents a fereign key in the database")
    product_pub_uuid: uuid.UUID = Field(title="Product Public UUID", description="Represents a public uuid of the product")
    product_name: str = Field(default="missing", min_length=2, max_length=100, title="Product Name")
    image: str = Field(default="/", title="Image Url", description="The image url of the product")
    price: float = Field(default=0.0, title="Product Price", description="The price of the product") 
    discount: float = Field(default=0.0, title="Product Discount", description="Percentage of the product discount")
    category_slug: str = Field(min_length=2, max_length=100, title="Category Slug")
    product_slug: str = Field(min_length=2, max_length=100, title="Product Slug")

class CartItemDetailsDTO(BaseDTO["CartItemDetailsDTO"]):
    size: uuid.UUID = Field(title="Size", description="Represents a fereign key in the database")
    product_pub_uuid: uuid.UUID = Field(title="Product Public UUID", description="Represents a public uuid of the product")
    product_name: str = Field(default="missing", min_length=2, max_length=100, title="Product Name")
    image: str = Field(default="/", title="Image Url", description="The image url of the product")
    price: float = Field(default=0.0, title="Product Price", description="The price of the product") 
    discount: float = Field(default=0.0, title="Product Discount", description="Percentage of the product discount")
    category_slug: str = Field(min_length=2, max_length=100, title="Category Slug")
    product_slug: str = Field(min_length=2, max_length=100, title="Product Slug")
