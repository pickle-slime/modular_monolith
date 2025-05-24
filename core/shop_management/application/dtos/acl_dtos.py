from core.shop_management.application.dtos.base_dto import BaseDTO, DTO

from core.user_management.application.dtos.user_management import UserDTO
from core.cart_management.application.dtos.cart_management import CartDTO, WishlistDTO, CartItemDTO, WishlistItemDTO

from pydantic import Field, model_validator
import uuid


class BaseItemDTO(BaseDTO[DTO]):
    color: str | None = Field(default=None, min_length=3, max_length=100, title="Item Color")
    qty: int | None = Field(default=None, ge=0, lt=100, title="QTY", description="QTY per item")
    size: uuid.UUID | None = Field(default=None, title="Size", description="Represents a fereign key in the database")

class ACLCartItemDTO(BaseItemDTO['CartItemDTO']):
    @classmethod
    def from_dto(cls, dto: CartItemDTO) -> 'ACLCartItemDTO':
        return cls(
            color=dto.color,
            qty=dto.qty,
            size=dto.size,
        )

class ACLWishlistItemDTO(BaseItemDTO['WishlistItemDTO']):
    pub_uuid: uuid.UUID | None = Field(default=None, title="Public UUID")
    @classmethod
    def from_dto(cls, dto: WishlistItemDTO) -> 'ACLWishlistItemDTO':
        return cls(
            pub_uuid=dto.pub_uuid,
            color=dto.color,
            qty=dto.qty,
            size=dto.size,
        )

class BaseItemCollectionDTO(BaseDTO[DTO]):
    pub_uuid: uuid.UUID | None = Field(default=None)
    total_price: float | None = Field(default=None, ge=0, title="Total Price")
    quantity: int | None = Field(default=None, ge=0, title="Quantity")

    user: uuid.UUID | None = Field(default=None, title="User", description="Contains a public uuid of external module")

class ACLCartDTO(BaseItemCollectionDTO):
    items: list[ACLCartItemDTO]| None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def from_dto(cls, dto: CartDTO) -> 'ACLCartDTO':
        return cls(
            total_price=float(dto.total_price) if dto.total_price else None,
            quantity=dto.quantity,
            items=[ACLCartItemDTO.from_dto(item) for item in dto.items] if dto.items else [],
            user=dto.user,
            pub_uuid=dto.pub_uuid,
        )
    

class ACLWishlistDTO(BaseItemCollectionDTO):
    items: list[ACLWishlistItemDTO] | None = Field(default=None, title="Contains a list of item DTOs")

    @classmethod
    def from_dto(cls, dto: WishlistDTO) -> 'ACLWishlistDTO':
        return cls(
            total_price=float(dto.total_price) if dto.total_price is not None else None,
            quantity=dto.quantity,
            items=[ACLWishlistItemDTO.from_dto(item) for item in dto.items] if dto.items else [],
            user=dto.user,
            pub_uuid=dto.pub_uuid,
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
