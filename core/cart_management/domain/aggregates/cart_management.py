from core.utils.domain.entity import Entity
from ..entities.cart_management import WishlistItem
from ..dtos.cart_management import AddToWishlistDomainDTO 

from decimal import Decimal
from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: Decimal | None = field(default=None)
    quantity: int | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    items: dict[uuid.UUID, WishlistItem] | None = field(default=None)

    _item_cls: type[WishlistItem] = WishlistItem

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
        self.total_price = (self.total_price or Decimal(0)) + Decimal(price * qty)

    def delete_item(self, item_uuid: uuid.UUID, qty: int = 1):
        if not self.items or item_uuid not in self.items:
            raise ValueError(f"{self.__class__.__name__}.{self.delete_item.__name__} can't find an item uuid in self.items")

        item = self.items[item_uuid]
        item_price = Decimal(item.price) if item.price else Decimal(0)

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
        self.total_price = max((self.total_price or Decimal(0)) - (item_price * qty), Decimal(0))


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
