from core.shop_management.application.dtos.acl_dtos import ACLWishlistDTO, ACLCartDTO
from core.shop_management.application.dtos.read_models import WishlistItemDetailsDTO, CartItemDetailsDTO

from core.shop_management.application.dtos.base_dto import BaseDTO
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

from pydantic import Field
import uuid

class ProductWishlistItemDTO(BaseDTO["ProductWishlistItemDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None, title="Public UUID")
    product_pub_uuid: uuid.UUID | None = Field(default=None, title="Prdouct Public UUID")
    color: str = Field(default="-", min_length=3, max_length=100, title="Item Color")
    qty: int = Field(default=0, ge=0, lt=100, title="QTY", description="QTY per item")
    size: uuid.UUID = Field(title="Size", description="Represents a fereign key in the database")
    image: str = Field(default="/", title="Image Url", description="The image url of the product")
    price: float = Field(default=0.0, title="Product Price", description="The price of the product")
    discount: float = Field(default=0.0, title="Product Discount", description="Percentage of the product discount")
    product_name: str = Field(default="missing", min_length=2, max_length=100, title="Product Name")
    get_absolute_url: str | None = Field(default=None, title="Absolute Url", description="Contains a path to the dedicated web page")

class ProductWishlistDTO(BaseDTO["ProductWishlistDTO"]):
    pub_uuid: uuid.UUID
    total_price: float = Field(default=0.0, ge=0, title="Total Price")
    quantity: int = Field(default=0, ge=0, title="Quantity")

    items: list[ProductWishlistItemDTO] | None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def merge(cls, acl_dto: ACLWishlistDTO, items: list[WishlistItemDetailsDTO], url_mapping_adapter: URLHost, media_url: str | None = None):
       return cls(
               pub_uuid=acl_dto.pub_uuid,
               total_price=acl_dto.total_price,
               quantity=acl_dto.quantity,
               items=cls._merging(acl_dto, items, url_mapping_adapter, media_url),
            )

    @classmethod
    def _merging(cls, acl_dto: ACLWishlistDTO, items: list[WishlistItemDetailsDTO], url_mapping_adapter: URLHost, media_url: str | None = None) -> list[ProductWishlistItemDTO]:
        details_map = {item.size: item for item in items}

        merged_items = []
        for acl_item in acl_dto.items or []:
            details = details_map.get(acl_item.size)
            if not details:
                merged_items.append(ProductWishlistItemDTO(
                    pub_uuid=acl_item.pub_uuid,
                    color=acl_item.color,
                    qty=acl_item.qty,
                    size=acl_item.size,
                    image=media_url if media_url else "/",
                    price=0.0,
                    discount=0.0,
                    product_name="missing",
                    get_absolute_url="/",
                ))
                continue

            product_absolute_url = url_mapping_adapter.get_absolute_url_of_product(details.category_slug, details.product_slug) if url_mapping_adapter else None
            merged_items.append(ProductWishlistItemDTO(
                pub_uuid=acl_item.pub_uuid,
                product_pub_uuid=details.product_pub_uuid,
                color=acl_item.color,
                qty=acl_item.qty,
                size=acl_item.size,
                image=media_url + details.image if media_url else details.image,
                price=details.price,
                discount=details.discount,
                product_name=details.product_name,
                get_absolute_url=product_absolute_url,
            ))

        return merged_items

class ProductCartItemDTO(BaseDTO["ProductCartItemDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None, title="Public UUID")
    product_pub_uuid: uuid.UUID | None = Field(default=None, title="Prdouct Public UUID")
    color: str = Field(default="-", min_length=3, max_length=100, title="Item Color")
    qty: int = Field(default=0, ge=0, lt=100, title="QTY", description="QTY per item")
    size: uuid.UUID = Field(title="Size", description="Represents a fereign key in the database")
    image: str = Field(default="/", title="Image Url", description="The image url of the product")
    price: float = Field(default=0.0, title="Product Price", description="The price of the product")
    discount: float = Field(default=0.0, title="Product Discount", description="Percentage of the product discount")
    product_name: str = Field(default="missing", min_length=2, max_length=100, title="Product Name")
    get_absolute_url: str | None = Field(default=None, title="Absolute Url", description="Contains a path to the dedicated web page")

class ProductCartDTO(BaseDTO["ProductCartDTO"]):
    pub_uuid: uuid.UUID
    total_price: float = Field(default=0.0, ge=0, title="Total Price")
    quantity: int = Field(default=0, ge=0, title="Quantity")

    items: list[ProductCartItemDTO] | None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def merge(cls, acl_dto: ACLCartDTO, items: list[CartItemDetailsDTO], url_mapping_adapter: URLHost, media_url: str | None = None):
       return cls(
               pub_uuid=acl_dto.pub_uuid,
               total_price=acl_dto.total_price,
               quantity=acl_dto.quantity,
               items=cls._merging(acl_dto, items, url_mapping_adapter, media_url),
            )

    @classmethod
    def _merging(cls, acl_dto: ACLCartDTO, items: list[CartItemDetailsDTO], url_mapping_adapter: URLHost, media_url: str | None = None) -> list[ProductCartItemDTO]:
        details_map = {item.size: item for item in items}

        merged_items = []
        for acl_item in acl_dto.items or []:
            details = details_map.get(acl_item.size)
            if not details:
                merged_items.append(ProductCartItemDTO(
                    pub_uuid=acl_item.pub_uuid,
                    color=acl_item.color,
                    qty=acl_item.qty,
                    size=acl_item.size,
                    image=media_url if media_url else "/",
                    price=0.0,
                    discount=0.0,
                    product_name="missing",
                    get_absolute_url="/",
                ))
                continue

            product_absolute_url = url_mapping_adapter.get_absolute_url_of_product(details.category_slug, details.product_slug) if url_mapping_adapter else None
            merged_items.append(ProductCartItemDTO(
                pub_uuid=acl_item.pub_uuid,
                product_pub_uuid=details.product_pub_uuid,
                color=acl_item.color,
                qty=acl_item.qty,
                size=acl_item.size,
                image=media_url + details.image if media_url else details.image,
                price=details.price,
                discount=details.discount,
                product_name=details.product_name,
                get_absolute_url=product_absolute_url,
            ))

        return merged_items
