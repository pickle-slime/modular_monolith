from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel

from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from django.db.models import Manager
from typing import Any

class DjangoCartItemMapper:
    @staticmethod
    def map_session_into_entity(session_cart_item: dict[str, Any]) -> CartItemVO:
        return CartItemVO(
            inner_uuid=session_cart_item.get("inner_uuid"),
            public_uuid=session_cart_item.get("public_uuid"),
            color=session_cart_item.get("color"),
            qty=session_cart_item.get("qty"),
            size=session_cart_item.get("size"),
            size_snapshot=session_cart_item.get("size_snapshot"),
        )
    
    @staticmethod
    def map_cart_items_into_entities(items: dict[str, Any]) -> list[CartItemVO]:
        return {str(entity.get("inner_uuid")): DjangoCartItemMapper.map_session_into_entity(entity) for entity in items}
    

class DjangoCartMapper:
    def __init__(self, session_adapter: RedisSessionHost):
        self.session_adapter = session_adapter

    def map_session_into_entity(self, session_cart: dict[str, Any]) -> CartEntity:
        return CartEntity(
            total_price=session_cart.get("total_price"),
            quantity=session_cart.get("quantity"),
            items=DjangoCartItemMapper.map_cart_items_into_entities(session_cart.get("items")),
            user=self.session_adapter.get("user_public_uuid")
        )
    
class DjangoWishlistItemMapper:
    @staticmethod
    def map_wishlist_item_into_entity(item: WishlistItemModel) -> WishlistItemEntity:
        size = item.size
        size_snapshot = {
            "length": size.length,
            "width": size.width,
            "height": size.height,
            "weight": size.weight,
        } if size else None

        return WishlistItemEntity(
            color=item.color,
            qty=item.qty,
            size=size,
            size_snapshot=size_snapshot,
        )

    @staticmethod
    def map_wishlist_items_into_entities(items: Manager[WishlistItemModel]) -> list[WishlistItemEntity] | None:
        if items:
            return {str(entity.inner_uuid): DjangoWishlistItemMapper.map_wishlist_item_into_entity(entity) for entity in items}
        return None

class DjangoWishlistMapper:
    @staticmethod
    def map_wishlist_into_entity(wishlist: WishlistModel, items: Manager[WishlistItemModel] = None):
        return WishlistEntity(
            inner_uuid=wishlist.inner_uuid,
            public_uuid=wishlist.public_uuid,
            total_price=wishlist.total_price,
            quantity=wishlist.quantity,
            user=wishlist.customer,
            items=DjangoWishlistItemMapper.map_wishlist_items_into_entities(items),
        )