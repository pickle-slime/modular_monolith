from core.cart_management.application.services.internal.event_driven_services import UserManagementService
from core.cart_management.application.exceptions import FailedCartInitializationError
from core.cart_management.infrastructure.dtos.event_driven_dtos import LoggedUserEventDTO
from core.cart_management.infrastructure.repositories.cart_management import DjangoCartRepository

from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.utils.infrastructure.adapters.serializer import SerializeAdapter

from pydantic import ValidationError
from celery import shared_task
from logging import Logger

logger = Logger("event handlers")

@shared_task(bind=True)
def handle_logged_user(self, event_data: dict):
    try:
        dto = LoggedUserEventDTO(**event_data)
    except ValidationError:
       logger.log(1, "Failed validation") 
       return

    try:
        service = UserManagementService(DjangoCartRepository(RedisSessionAdapter(RedisAdapter(), SerializeAdapter())))
        service.handle_logged_user(dto)   
    except FailedCartInitializationError as e:
        logger.log(1, f"Failed service initialization: {e.raw_msg}")
        raise self.retry(exc=e, countdown=5)
