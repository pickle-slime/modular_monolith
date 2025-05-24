from core.order_management.domain.entity import Entity

from decimal import Decimal
from dataclasses import dataclass

@dataclass(kw_only=True)
class Shipment(Entity):
    tracking_number: str
    shipment_id: str
    transaction_id: str
    label_url: str
    shipping_cost: Decimal
