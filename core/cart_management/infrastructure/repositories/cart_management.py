from core.cart_management.domain.interfaces.i_repositories.i_cart_management import IWishlistRepository, IWishlistItemRepository, ICartRepository, ICartItemRepository
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity, CartItem as CartItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel
from ..dtos.cart_management import RedisCartDTO

from ....utils.domain.interfaces.hosts.redis import RedisSessionHost

from django.db.models import Manager
from typing import Any
import uuid


class DjangoCartItemRepository(ICartItemRepository):
    def __init__(self, session_adapter: RedisSessionHost):
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
    def __init__(self, session_adapter: RedisSessionHost):
        self.session_adapter = session_adapter

    def map_session_into_entity(self, session_cart: dict[str, Any]) -> CartEntity:
        return CartEntity(
            total_price=session_cart.get("total_price"),
            quantity=session_cart.get("quantity"),
            items=DjangoCartItemRepository.map_cart_items_into_entities(session_cart.get("items")),
            user=self.session_adapter.get("user_public_uuid")
        )

    def fetch_cart(self) -> CartEntity:
        raw_cart = self.session_adapter.get("cart")
        if raw_cart:
            return self.map_session_into_entity(RedisCartDTO)
        else:
            return CartEntity(inner_uuid=None, public_uuid=None)
        
    def save(self, cart_entity: CartEntity) -> None:
        dto = RedisCartDTO.from_entity(cart_entity)
        self.session_adapter.set("cart", dto.model_dump())


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
            size=size,
            size_snapshot=size_snapshot,
        )

    @staticmethod
    def map_wishlist_items_into_entities(items: Manager[WishlistItemModel]) -> list[WishlistItemEntity]:
        return [DjangoWishlistItemRepository.map_wishlist_item_into_entity(entity) for entity in items]

class DjangoWishlistRepository(IWishlistRepository):
    @staticmethod
    def map_wishlist_into_entity(wishlist: WishlistModel):
        return WishlistEntity(
            inner_uuid=wishlist.inner_uuid,
            public_uuid=wishlist.public_uuid,
            total_price=wishlist.total_price,
            quantity=wishlist.quantity,
            user=wishlist.customer.public_uuid,
            items=DjangoWishlistItemRepository.map_wishlist_items_into_entities(wishlist.orderproduct_set.all().select_related('size__product__category')),
        )

    def fetch_wishlist_by_user(self, public_uuid: uuid.UUID = None) -> WishlistEntity:
        wishlist = WishlistModel.objects.filter(customer__public_uuid=public_uuid).first()
            
        if wishlist:
            return self.map_wishlist_into_entity(wishlist)
        else:
            return WishlistEntity(inner_uuid=None, public_uuid=None)


