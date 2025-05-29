from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.domain.value_objects.cart_management import CartItem as CartItemVO
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel

from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from decimal import Decimal
from django.db.models import Manager
from typing import Any
import uuid

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
        if items:
            return {str(entity.get("inner_uuid")): DjangoCartItemMapper.map_session_into_entity(entity) for entity in items}
        return list()
    

class DjangoCartMapper:
    def __init__(self, session_adapter: RedisSessionHost):
        self.session_adapter = session_adapter

    def map_session_into_entity(self, session_cart: dict[str, Any]) -> CartEntity:
        return CartEntity(
            inner_uuid=session_cart.get("inner_uuid"),
            public_uuid=session_cart.get("public_uuid"),
            total_price=session_cart.get("total_price"),
            quantity=session_cart.get("quantity"),
            items=DjangoCartItemMapper.map_cart_items_into_entities(session_cart.get("items")),
            user=self.session_adapter.get("user_public_uuid")
        )
    
class DjangoWishlistItemMapper:
    @staticmethod
    def map_wishlist_item_into_entity(item: WishlistItemModel) -> WishlistItemEntity:
        return WishlistItemEntity(
            inner_uuid=item.inner_uuid,
            public_uuid=item.public_uuid,
            color=item.color,
            qty=item.qty,
            size=item.size.public_uuid,
        )

    @staticmethod
    def map_wishlist_items_into_entities(items: Manager[WishlistItemModel]) -> dict[uuid.UUID, WishlistItemEntity]:
        if items:
            return {uuid.UUID(str(model.public_uuid)): DjangoWishlistItemMapper.map_wishlist_item_into_entity(model) for model in items}
        return dict()

    @staticmethod
    def map_raw_items_into_entities(rows: list[tuple]) -> dict[uuid.UUID, WishlistItemEntity]:
        return {
            uuid.UUID(str(public_uuid)): WishlistItemEntity(
                inner_uuid=uuid.UUID(str(inner_uuid)),
                public_uuid=uuid.UUID(str(public_uuid)),
                color=color,
                qty=qty,
                size=uuid.UUID(str(size_id)) if size_id else None,
            )
            for (inner_uuid, public_uuid, color, qty, size_id) in rows
        }

class DjangoWishlistMapper:
    @staticmethod
    def map_wishlist_into_entity(wishlist: WishlistModel, items: Manager[WishlistItemModel] | None = None) -> WishlistEntity:
        return WishlistEntity(
            inner_uuid=wishlist.inner_uuid,
            public_uuid=wishlist.public_uuid,
            total_price=wishlist.total_price,
            quantity=wishlist.quantity,
            user=wishlist.customer.public_uuid,
            items=DjangoWishlistItemMapper.map_wishlist_items_into_entities(items),
        )

    @staticmethod
    def map_raw_wishlist_into_entity(
        row: tuple,
        items: dict[uuid.UUID, WishlistItemEntity]
    ) -> WishlistEntity:
        return WishlistEntity(
            inner_uuid=row[0],
            public_uuid=row[1],
            user=row[2],
            total_price=row[3],
            quantity=row[4],
            items=items,
        )
