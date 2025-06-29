from config import BOUNDED_CONTEXTS
from core.utils.domain.interfaces.hosts.event_bus import CeleryEventBusHost

from logging import Logger
import importlib

logger = Logger("register_event_handlers")

def register_event_handlers(bus: CeleryEventBusHost) -> None:
    for bc in BOUNDED_CONTEXTS:
        try:
            module_path = f"core.{bc}.infrastructure.celery.subscription.acl_event_subscription"
            subscription_module = importlib.import_module(module_path)
            subscription_func = getattr(subscription_module, "register_event_handlers")
            subscription_func(bus)
        except (ModuleNotFoundError, AttributeError) as e:
            logger.warning(f"[Subscription] Skipping {bc}: {e} [Subscription]")
