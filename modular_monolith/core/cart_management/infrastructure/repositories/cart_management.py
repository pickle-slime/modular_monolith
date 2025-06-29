from core.cart_management.domain.interfaces.i_repositories.i_cart_management import IWishlistRepository, ICartRepository
from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity, Cart as CartEntity
from core.cart_management.domain.entities.cart_management import  WishlistItem as WishlistItemEntity
from core.cart_management.application.exceptions import NotFoundWishlistError, NotFoundCartError, InvalidSessionAdapter
from ..dtos.cart_management import RedisCartDTO, RedisCartItemDTO
from ..mappers.cart_management import DjangoWishlistMapper, DjangoWishlistItemMapper
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.utils.exceptions import RedisException

from django.db import transaction, connection

from dataclasses import asdict
import uuid

class DjangoCartRepository(ICartRepository):
    def __init__(self, session_adapter: RedisSessionHost):
        self.session_adapter = session_adapter

    def fetch_cart(self) -> CartEntity:
        cart = self.session_adapter.get("cart", dtos=[RedisCartDTO, RedisCartItemDTO])
        if cart:
            return cart.to_entity()
        else:
            raise NotFoundCartError(f"didn't find cart with ({self.session_adapter.session_key})")
        
    def save(self, cart_entity: CartEntity) -> None:
        try:
            cart = RedisCartDTO.from_entity(cart_entity)
            self.session_adapter.set("cart", cart)
        except RedisException as e:
            raise InvalidSessionAdapter(e.raw_msg)

    def session_key(self) -> str:
        return self.session_adapter.session_key

class DjangoWishlistRepository(IWishlistRepository):
    def fetch_wishlist_by_user(self, public_uuid: uuid.UUID | None = None) -> WishlistEntity:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    w."inner_uuid",
                    w."public_uuid",
                    w."customer_id",
                    COALESCE(SUM(
                        (
                            wp."qty" * p."price"
                        ) * (
                            1 - (p."discount" / 100.0)
                        )
                    ), 0.0) AS total_price,
                    COALESCE(SUM(wp."qty"), 0) AS quantity
                FROM "cart_management_wishlist" w
                LEFT OUTER JOIN "cart_management_wishlistorderproduct" wp
                    ON w."inner_uuid" = wp."wishlist_id"
                LEFT OUTER JOIN "shop_management_productsizes" ps
                    ON wp."size_id" = ps."public_uuid"
                LEFT OUTER JOIN "shop_management_product" p
                    ON ps."product_id" = p."inner_uuid"
                WHERE w."customer_id" = %s
                GROUP BY w."inner_uuid", w."public_uuid", w."customer_id"
                LIMIT 1;
                """,
                [str(public_uuid)]
            )
            row = cursor.fetchone()

        if not row:
            raise NotFoundWishlistError(f"didn't find wishlist by customer__public_uuid ({public_uuid})")

        wishlist_inner_uuid = row[0]

        items = self._fetch_wishlist_items(wishlist_inner_uuid)

        return DjangoWishlistMapper.map_raw_wishlist_into_entity(row, items)

    def _fetch_wishlist_items(self, wishlist_inner_uuid: uuid.UUID) -> dict[uuid.UUID, WishlistItemEntity]:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    wp."inner_uuid",
                    wp."public_uuid",
                    wp."color",
                    wp."qty",
                    wp."size_id"
                FROM "cart_management_wishlistorderproduct" wp
                WHERE wp."wishlist_id" = %s
                """,
                [str(wishlist_inner_uuid)]
            )
            rows = cursor.fetchall()

        return DjangoWishlistItemMapper.map_raw_items_into_entities(rows)

    @transaction.atomic()
    def save(self, wishlist: WishlistEntity):
        wishlist_dict = asdict(wishlist)
        items = wishlist.items
        self.insert_wishlist(wishlist_dict)

        if items:
            item_dicts = []
            for key, item in items.items():
                item_dict = asdict(item)
                item_dict["wishlist_id"] = wishlist.inner_uuid
                item_dicts.append(item_dict)
            self.bulk_insert_items(item_dicts)

        if wishlist._removed_items:
            self.bulk_delete_items(wishlist._removed_items)

    def bulk_insert_items(self, item_dicts: list[dict]):
        insert_sql = '''
            INSERT INTO cart_management_wishlistorderproduct (
                inner_uuid, public_uuid, color, qty, size_id, wishlist_id
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (inner_uuid) DO NOTHING
        '''

        values = [
            (
                item["inner_uuid"],
                item["public_uuid"],
                item["color"],
                item["qty"],
                item["size"],
                item["wishlist_id"],
            )
            for item in item_dicts
        ]

        with connection.cursor() as cursor:
            for value in values:
                cursor.execute(insert_sql, value)

    def insert_wishlist(self, wishlist: dict):
        sql = '''
            INSERT INTO cart_management_wishlist(
                inner_uuid, public_uuid, customer_id
            ) VALUES (%s, %s, %s)
            ON CONFLICT (inner_uuid) DO UPDATE SET
                public_uuid = EXCLUDED.public_uuid,
                customer_id = EXCLUDED.customer_id
        '''

        values = (
            wishlist["inner_uuid"],
            wishlist["public_uuid"],
            wishlist["user"],
        )

        with connection.cursor() as cursor:
            cursor.execute(sql, values)

    def bulk_delete_items(self, uuids: set[uuid.UUID]):
        delete_sql = '''
            DELETE FROM cart_management_wishlistorderproduct
            WHERE inner_uuid = ANY(%s)
        '''
        with connection.cursor() as cursor:
            cursor.execute(delete_sql, (list(uuids),))
