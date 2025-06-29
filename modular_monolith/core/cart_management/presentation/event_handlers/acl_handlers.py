from core.cart_management.application.services.internal.event_driven_services import UserManagementService
from core.cart_management.application.exceptions import FailedCartInitializationError
from core.cart_management.application.dtos.acl_event_driven_dtos import LoggedUserEventDTO, SignedUPUserEventDTO
from core.cart_management.infrastructure.repositories.cart_management import DjangoCartRepository, DjangoWishlistRepository

from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.utils.infrastructure.adapters.serializer import SerializeAdapter

from core.user_management.application.events.acl_events import NewUserACLEvent, UserLoggedInACLEvent

from pydantic import ValidationError
from celery import shared_task
from logging import Logger

logger = Logger("event handlers")

@shared_task(bind=True)
def handle_logged_user(self, event_data: UserLoggedInACLEvent):
    try:
        dto = LoggedUserEventDTO.from_event(event_data)
    except ValidationError:
       logger.error("Failed validation") 
       return

    try:
        service = UserManagementService(
                DjangoCartRepository(
                    RedisSessionAdapter(
                        redis_adapter=RedisAdapter(), 
                        serialize_adapter=SerializeAdapter(), 
                        session_key=dto.session_key
                        )
                    ),
                )
        service.handle_logged_user(dto)   
    except FailedCartInitializationError as e:
        logger.log(1, f"Failed service initialization: {e.raw_msg}")
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def handle_registered_user(self, event_data: NewUserACLEvent):
    try:
        dto = SignedUPUserEventDTO.from_event(event_data)
    except ValidationError:
       logger.error("Failed validation") 
       return

    try:
        service = UserManagementService(wishlist_repository=DjangoWishlistRepository())
        service.handle_registered_user(dto)   
    except FailedCartInitializationError as e:
        logger.log(1, f"Failed service initialization: {e.raw_msg}")
        raise self.retry(exc=e, countdown=5)
