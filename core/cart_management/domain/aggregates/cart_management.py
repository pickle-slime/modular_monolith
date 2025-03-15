from core.utils.domain.entity import Entity
from ..entities.cart_management import WishlistItem
from ..value_objects.cart_management import Size as SizeVO

from decimal import Decimal
from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Wishlist(Entity):
    total_price: Decimal = field(default=None)
    quantity: int = field(default=None)

    user: uuid.UUID = field(default=None)

    items: dict[uuid.UUID, WishlistItem] = field(default=None)

    def add_item(self, item_uuid: uuid.UUID, price: float, color: str, qty: int, image: str, size: SizeVO) -> tuple['Wishlist', WishlistItem]:
        if item_uuid in self.items:
            existing_item = self.items[item_uuid]
            existing_item.qty += qty
        else:
            self.items[item_uuid] = WishlistItem(color=color, qty=qty, image=image, size=size)

        self.quantity += qty
        self.total_price += price * qty

        return self, self.items[item_uuid]

    def delete_item(self, item_inner_uuid: uuid.UUID, qty: int = None) -> bool:
        if item_inner_uuid in self.items:
            item = self.items.pop(item_inner_uuid)
            self.quantity -= item.qty if not qty else qty
            self.total_price -= item.qty * item.price
            return True
        return False

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
