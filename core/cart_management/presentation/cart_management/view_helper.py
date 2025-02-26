from django.http import HttpRequest

from core.cart_management.application.services.internal.cart_management import ItemCollectionService
from core.cart_management.presentation.acl_factory import CartManagementACLFactory
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.user_management.presentation.acl_factory import UserManagementACLFactory
from core.utils.application.base_factories import BaseServiceFactory

from core.shop_management.presentation.acl_factory import ShopManagementACLFactory

SERVICE_FACTORY = BaseServiceFactory(
    services={
        "product_acl": ShopManagementACLFactory.create_product_acl(),
        "cart_acl": None,
        "wishlist_acl": CartManagementACLFactory.create_wishlist_acl(),
        "user_acl": UserManagementACLFactory.create_user_acl(),
    },
    adapters={
        "session_adapter": None
    }
)

def initiate_item_collection_service(request: HttpRequest) -> ItemCollectionService:
    session_adapter = RedisSessionAdapter(RedisAdapter(), session_key=request.session.session_key)
    SERVICE_FACTORY._services["cart_acl"] = CartManagementACLFactory.create_cart_acl(session_adapter)
    SERVICE_FACTORY._adapters["session_adapter"] = RedisSessionAdapter(session_adapter, request.session_key)
    return SERVICE_FACTORY.create_service(ItemCollectionService)