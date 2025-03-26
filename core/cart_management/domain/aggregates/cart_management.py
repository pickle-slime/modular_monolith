from core.utils.domain.entity import Entity
from ..entities.cart_management import WishlistItem, Size as SizeEntity

from decimal import Decimal
from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: Decimal | None = field(default=None)
    quantity: int | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    items: dict[uuid.UUID, WishlistItem] | None = field(default=None)

    def add_item(
        self, item_uuid: uuid.UUID, price: float, color: str, qty: int, image: str, size: SizeEntity
    ) -> tuple["Wishlist", WishlistItem]:
        if self.items is None:
            self.items = {}

        if item_uuid in self.items:
            existing_item = self.items[item_uuid]
            existing_item.qty += qty
        else:
            self.items[item_uuid] = WishlistItem(color=color, qty=qty, image=image, size=size)

        self.quantity = (self.quantity or 0) + qty
        self.total_price = (self.total_price or Decimal(0)) + Decimal(price * qty)

        return self, self.items[item_uuid]

    def delete_item(self, item_uuid: uuid.UUID, qty: int | None = None) -> bool:
        if not self.items or item_uuid not in self.items:
            return False

        item = self.items[item_uuid]
        item_price = Decimal(item.price) if item.price else Decimal(0)

        if qty is None or qty >= item.qty:
            del self.items[item_uuid]
            qty = item.qty
        else:
            item.qty -= qty

        self.quantity = max((self.quantity or 0) - qty, 0)
        self.total_price = max((self.total_price or Decimal(0)) - (item_price * qty), Decimal(0))

        return True

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
