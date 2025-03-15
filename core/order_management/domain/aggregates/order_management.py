from core.utils.domain.entity import Entity
from ..entities.order_management import Shipment
from ..value_objects.order_management import BillingAddress, OrderStatus

from decimal import Decimal
from datetime import datetime
from dataclasses import field
import uuid

class Order(Entity):
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    total_price: Decimal = field(default=None)
    stripe_payment_intent_id: str = field(default=None)
    status: OrderStatus = field(default=None)
    created_at: datetime = field(default=None)
    updated_at: datetime = field(default=None)

    user: uuid.UUID = field(default=None)

    shipment: Shipment = field(default=None)
    billing_address: BillingAddress = field(default=None)
