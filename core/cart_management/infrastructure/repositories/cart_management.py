from core.cart_management.domain.interfaces.i_repositories.i_cart_management import IWishlistRepository, IWishlistItemRepository, ICartRepository, ICartItemRepository
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity, Cart as CartEntity, CartItem as CartItemEntity
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel
from core.utils.domain.value_objects.common import ForeignUUID

from ....utils.infrastructure.adapters.redis import RedisSessionAdapter

from django.db.models import Manager
from typing import Any
import uuid


class DjangoCartItemRepository(ICartItemRepository):
    def __init__(self, session_adapter: RedisSessionAdapter):
        self.session_adapter = session_adapter

    @staticmethod
    def map_session_into_entity(session_cart_item: dict[str, Any]) -> CartItemEntity:
        return CartItemEntity(
            inner_uuid=session_cart_item.get("inner_uuid"),
            public_uuid=session_cart_item.get("public_uuid"),
            color=session_cart_item.get("color"),
            qty=session_cart_item.get("qty"),
            size=session_cart_item.get("size"),
            size_snapshot=session_cart_item.get("size_snapshot"),
        )
    
    @staticmethod
    def map_cart_items_into_entities(items: dict[str, Any]) -> list[CartItemEntity]:
        return [DjangoCartItemRepository.map_session_into_entity(entity) for entity in items]

class DjangoCartRepository(ICartRepository):
    def __init__(self, session_adapter: RedisSessionAdapter):
        self.session_adapter = session_adapter

    def map_session_into_entity(self, session_cart: dict[str, Any], user_inner_uuid: uuid.UUID = None) -> CartEntity:
        return CartEntity(
            total_price=session_cart.get("total_price"),
            quantity=session_cart.get("quantity"),
            items=DjangoCartItemRepository.map_cart_items_into_entities(session_cart.get("items")),
            user=ForeignUUID(user_inner_uuid, self.session_adapter.get("user_public_uuid")) if user_inner_uuid else self.session_adapter.get("user_public_uuid")
        )

    def fetch_cart(self) -> CartEntity:
        raw_cart = self.session_adapter.get("cart")
        if raw_cart:
            return self.map_session_into_entity(raw_cart)
        else:
            return CartEntity(inner_uuid=None, public_uuid=None)


class DjangoWishlistItemRepository(IWishlistItemRepository):
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
            size=ForeignUUID(size.inner_uuid, size.public_uuid),
            size_snapshot=size_snapshot,
        )

    @staticmethod
    def map_wishlist_items_into_entities(items: Manager[WishlistItemModel]) -> list[WishlistItemEntity]:
        return [DjangoWishlistItemRepository.map_wishlist_item_into_entity(entity) for entity in items]

class DjangoWishlistRepository(IWishlistRepository):
    @staticmethod
    def map_wishlist_into_entity(wishlist: WishlistModel):
        user = wishlist.customer
        return WishlistEntity(
            inner_uuid=wishlist.inner_uuid,
            public_uuid=wishlist.public_uuid,
            total_price=wishlist.total_price,
            quantity=wishlist.quantity,
            user=ForeignUUID(user.inner_uuid, user.public_uuid),
            items=DjangoWishlistItemRepository.map_wishlist_items_into_entities(wishlist.orderproduct_set.all().select_related('size__product__category')),
        )

    def fetch_wishlist_by_user(self, inner_uuid: uuid.UUID = None, public_uuid: uuid.UUID = None) -> WishlistEntity:
        if inner_uuid:
            wishlist = WishlistModel.objects.filter(customer__inner_uuid=inner_uuid).first()
        elif public_uuid:
            wishlist = WishlistModel.objects.filter(customer__public_uuid=public_uuid).first()
            
        if wishlist:
            return self.map_wishlist_into_entity(wishlist)
        else:
            return WishlistEntity(inner_uuid=None, public_uuid=None)


