from core.order_management.domain.entity import Entity
from ..entities.order_management import Shipment
from ..value_objects.order_management import BillingAddress, OrderStatus

from decimal import Decimal
from datetime import datetime
from dataclasses import field
import uuid

class Order(Entity):
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    total_price: Decimal | None  = field(default=None)
    stripe_payment_intent_id: str | None  = field(default=None)
    status: OrderStatus | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    user: uuid.UUID | None = field(default=None)

    shipment: Shipment | None = field(default=None)
    billing_address: BillingAddress | None = field(default=None)
