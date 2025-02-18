from django.http import HttpRequest

from core.cart_management.application.services.internal.cart_management import ItemCollectionService
from core.cart_management.infrastructure.repositories.cart_management import DjangoCartRepository, DjangoWishlistRepository
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.user_management.infrastructure.repositories.user_management import DjangoUserRepository
from core.utils.application.base_service import BaseService
from core.utils.application.base_factories import BaseServiceFactory

from core.shop_management.presentation.acl_factory import ShopManagementACLFactory

SERVICE_FACTORY = BaseServiceFactory(
    repositories={
        "cart_repository": DjangoCartRepository,
        "wishlist_repository": DjangoWishlistRepository,
        "product_acl": ShopManagementACLFactory.create_product_acl(),
    }, 
    services={
        "base_service": BaseService,
    }
)

def initiate_item_collection_service(request: HttpRequest) -> ItemCollectionService:
    session_adapter = RedisSessionAdapter(RedisAdapter(), session_key=request.session.session_key)
    
    repository_args = {
        "cart_repository": {
            "session_adapter": session_adapter,
        }
    }
    service_args = {
        "base_service": {
            "session_adapter": session_adapter,
            "user_repository": DjangoUserRepository()
        }
    }
    
    return SERVICE_FACTORY.create_service(ItemCollectionService, repository_args=repository_args, service_args=service_args)