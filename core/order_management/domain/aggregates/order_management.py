from ....utils.domain.entity import Entity
from ....utils.domain.value_objects.common import ForeignUUID
from ..entities.order_management import BillingAddress, Shipment

from decimal import Decimal
from datetime import datetime
import uuid

class Order(Entity):
    total_price: Decimal
    stripe_payment_intent_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    user: ForeignUUID | uuid.UUID

    shipment: Shipment
    billing_address: BillingAddress
