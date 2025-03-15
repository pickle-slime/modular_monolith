from django.http import HttpRequest

from core.cart_management.application.services.internal.cart_management import ItemCollectionService
from core.cart_management.infrastructure.repositories.cart_management import DjangoWishlistRepository, DjangoCartRepository
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.user_management.presentation.acl_factory import UserManagementACLFactory
from core.utils.application.base_factories import BaseServiceFactory

from core.shop_management.presentation.acl_factory import ShopManagementACLFactory

SERVICE_FACTORY = BaseServiceFactory(
    services={
        "product_acl": ShopManagementACLFactory.create_product_acl(),
        "cart_repository": None,
        "wishlist_repository": DjangoWishlistRepository(),
        "user_acl": UserManagementACLFactory.create_user_acl(),
    },
    adapters={
        "session_adapter": None
    }
)

def initiate_item_collection_service(request: HttpRequest) -> ItemCollectionService:
    session_adapter = RedisSessionAdapter(session_key=request.session.session_key)
    SERVICE_FACTORY._services["cart_acl"] = DjangoCartRepository(session_adapter)
    SERVICE_FACTORY._adapters["session_adapter"] = session_adapter
    return SERVICE_FACTORY.create_service(ItemCollectionService)