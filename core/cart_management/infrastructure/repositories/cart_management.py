from core.cart_management.domain.interfaces.i_repositories.i_cart_management import IWishlistRepository, ICartRepository
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, WishlistItem as WishlistItemEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel
from ..dtos.cart_management import RedisCartDTO
from ..mappers.cart_management import DjangoWishlistMapper
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost

from django.db import transaction

import uuid


class DjangoCartRepository(ICartRepository):
    def __init__(self, session_adapter: RedisSessionHost):
        self.session_adapter = session_adapter

    def fetch_cart(self) -> CartEntity:
        raw_cart = self.session_adapter.get("cart")
        if raw_cart:
            return RedisCartDTO(**raw_cart).to_entity()
        else:
            return CartEntity()
        
    def save(self, cart_entity: CartEntity) -> None:
        dto = RedisCartDTO.from_entity(cart_entity)
        self.session_adapter.set("cart", dto.model_dump())


class DjangoWishlistRepository(IWishlistRepository):
    def fetch_wishlist_by_user(self, public_uuid: uuid.UUID | None = None) -> WishlistEntity:
        wishlist = WishlistModel.objects.filter(customer__public_uuid=public_uuid).first()
            
        if wishlist:
            return DjangoWishlistMapper.map_wishlist_into_entity(wishlist)
        else:
            return WishlistEntity()

    @transaction.atomic  
    def save(self, wishlist: WishlistEntity | None = None, wishlist_items: list[WishlistItemEntity] | None = None) -> None:
        if wishlist:
            wishlist_data = dict(wishlist)
            wishlist_model, created = WishlistModel.objects.update_or_create(
                public_uuid=wishlist_data.get("public_uuid"), defaults=wishlist_data
            )

        if wishlist_items:
            wishlist_item_models = []
            for item in wishlist_items:
                item_data = dict(item)
                item_data["wishlist"] = wishlist_model.pk
                wishlist_item_models.append(WishlistItemModel(**item_data))
        
        WishlistItemModel.objects.bulk_create(wishlist_item_models, ignore_conflicts=True)

        


