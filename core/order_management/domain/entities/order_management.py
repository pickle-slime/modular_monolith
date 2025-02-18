from ....utils.domain.entity import Entity

from decimal import Decimal
from dataclasses import dataclass

@dataclass(kw_only=True)
class BillingAddress(Entity):
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    country: str
    zip_code: str
    telephone: str

@dataclass(kw_only=True)
class Shipment(Entity):
    tracking_number: str
    shipment_id: str
    transaction_id: str
    label_url: str
    shipping_cost: Decimal