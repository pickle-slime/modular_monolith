from shippo import components

from dataclasses import dataclass, field
from decimal import Decimal

@dataclass(frozen=True)
class Size:
    length: Decimal = field(default=None)
    width: Decimal = field(default=None)
    height: Decimal = field(default=None)
    weight: Decimal = field(default=None)

@dataclass(frozen=True)
class CartItem:
    color: str = field(default=None)
    qty: int = field(default=None)
    image: str = field(default=None)
    price: Decimal = field(default=None)

    size: Size = field(default_factory=Size)

    def to_shippo_parcel(self):
        return components.ParcelCreateRequest(
            length = f"{self.length}",  
            width = f"{self.width}",
            height = f"{self.height}",
            weight = f"{self.weight}",
            distance_unit = components.DistanceUnitEnum.IN,
            mass_unit = components.WeightUnitEnum.LB,
        )
    
