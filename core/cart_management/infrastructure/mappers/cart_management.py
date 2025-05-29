from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity
from core.cart_management.domain.entities.cart_management import WishlistItem as WishlistItemEntity
from core.cart_management.presentation.cart_management.models import WishList as WishlistModel, WishListOrderProduct as WishlistItemModel

from django.db.models import Manager
import uuid
    
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
