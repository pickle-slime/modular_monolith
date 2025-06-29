from core.utils.infrastructure.adapters.event_bus import CeleryEventBusHost
from core.cart_management.presentation.event_handlers.acl_handlers import *

from core.user_management.application.events.acl_events import NewUserACLEvent, UserLoggedInACLEvent

def register_event_handlers(bus: CeleryEventBusHost):
    bus.subscribe(UserLoggedInACLEvent, handle_logged_user)
    bus.subscribe(NewUserACLEvent, handle_registered_user)


