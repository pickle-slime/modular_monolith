from core.cart_management.domain.entity import Entity
from ..entities.cart_management import WishlistItem, CartItem
from ..dtos.cart_management import AddToWishlistDomainDTO, AddToCartDomainDTO

from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Cart(Entity):
    total_price: Decimal = field(default=Decimal("0.0"))
    quantity: int = field(default=0)

    user: uuid.UUID

    items: dict[uuid.UUID, CartItem] = field(default_factory=dict)

    _item_cls: type[CartItem] = CartItem

    @property
    def _total_price(self) -> Decimal | None:
        if isinstance(self.total_price, Decimal):
            return self.total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @Entity.require_fields()
    def add_item(
        self, 
        domain_dto: AddToCartDomainDTO,
        qty: int,
        price: Decimal,
        item_uuid: uuid.UUID | None = None,
    ):
        if self.items is None:
            self.items = {}

        item_uuid = item_uuid if item_uuid else uuid.uuid4()

        if item_uuid in self.items:
            existing_item = self.items[item_uuid]
            existing_item.qty = (existing_item.qty or 0) + qty
        else:
            self.items[item_uuid] = self._item_cls.map_domain_dto(domain_dto)

        self.quantity = (self.quantity or 0) + qty
        self.total_price = (self._total_price or Decimal(0)) + Decimal(price * qty)

    @Entity.require_fields()
    def delete_item(self, item_uuid: uuid.UUID, price: Decimal, qty: int = 1):
        if not self.items:
            raise ValueError(f"{self.__class__.__name__}.{self.delete_item.__name__} can't find an item uuid in self.items")

        item = self.items[item_uuid]

        if item.qty and qty >= item.qty:
            try:
                del self.items[item_uuid]
            except KeyError:
                raise KeyError(f"{self.__class__.__name__}.{self.delete_item.__name__} can't find an item by item_uuid")
            qty = item.qty
        else:
            if isinstance(item.qty, int):
                item.qty -= qty
            else:
                item.qty = qty

        self.quantity = max((self.quantity or 0) - qty, 0)
        self.total_price = max((self._total_price or Decimal(0)) - (price * qty), Decimal(0))


@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: Decimal | None = field(default=None)
    quantity: int | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    items: dict[uuid.UUID, WishlistItem] | None = field(default=None)

    _item_cls: type[WishlistItem] = WishlistItem
    _removed_items: set[uuid.UUID] = field(default_factory=set, init=False)

    @property
    def _total_price(self) -> Decimal | None:
        if isinstance(self.total_price, Decimal):
            return self.total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @Entity.require_fields()
    def add_item(
        self, 
        raw_wishlist_item: AddToWishlistDomainDTO,
        qty: int,
        price: Decimal,
        item_uuid: uuid.UUID | None = None,
    ):
        if self.items is None:
            self.items = {}

        item_uuid = item_uuid if item_uuid else uuid.uuid4()

        if item_uuid in self.items:
            existing_item = self.items[item_uuid]
            existing_item.qty = (existing_item.qty or 0) + qty
        else:
            self.items[item_uuid] = self._item_cls.map_domain_dto(raw_wishlist_item)

        self.quantity = (self.quantity or 0) + qty
        self.total_price = (self._total_price or Decimal(0)) + Decimal(price * qty)

    @Entity.require_fields()
    def delete_item(self, item_uuid: uuid.UUID, price: Decimal, qty: int = 1):
        if not self.items:
            raise ValueError(f"{self.__class__.__name__}.{self.delete_item.__name__} can't find an item uuid in self.items")

        item = self.items[item_uuid]

        if item.qty and qty >= item.qty:
            try:
                inner_uuid = self.items[item_uuid].inner_uuid
                self._removed_items.add(inner_uuid)
                del self.items[item_uuid]
            except KeyError:
                raise KeyError(f"{self.__class__.__name__}.{self.delete_item.__name__} can't find an item by item_uuid")
            qty = item.qty
        else:
            if isinstance(item.qty, int):
                item.qty -= qty
            else:
                item.qty = qty

        self.quantity = max((self.quantity or 0) - qty, 0)
        self.total_price = max((self._total_price or Decimal(0)) - Decimal(price * qty), Decimal(0))


    # def get_list_of_parcels(self, item_collection):
    #     parcels = []
    #     order_products = item_collection.orderproduct_set.all()

    #     for order_product in order_products:
    #         if order_product.size:
    #             parcel_data = order_product.size.to_shippo_parcel()
    #             for _ in range(order_product.qty):
    #                 parcels.append(parcel_data)
    #         else:
    #             raise ValueError(f"Order product {order_product.id} does not have a size assigned.")
                
    #     return parcels
