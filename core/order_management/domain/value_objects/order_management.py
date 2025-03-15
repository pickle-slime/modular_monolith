
from dataclasses import dataclass, field
from enum import Enum
import re

class OrderStatus(str, Enum):
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

@dataclass(frozen=True)
class PhoneField:
    value: str

    def __post_init__(self):
        if re.match(r"^\+?\d{7,15}$", self.value):
            raise ValueError(f"Invalide phone number {self.value}")

@dataclass(frozen=True)
class BillingAddress:
    address: str = field(default=None)
    city: str = field(default=None)
    state: str = field(default=None)
    country: str = field(default=None)
    zip_code: str = field(default=None)
    phone: PhoneField = field(default=None)