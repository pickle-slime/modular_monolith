from shippo import components

from dataclasses import dataclass, field
from decimal import Decimal

@dataclass(frozen=True)
class Size:
    length: Decimal = field(default=Decimal(0.0))
    width: Decimal = field(default=Decimal(0.0))
    height: Decimal = field(default=Decimal(0.0))
    weight: Decimal = field(default=Decimal(0.0))

@dataclass(frozen=True)
class CartItem:
    color: str = field(default=None)
    qty: int = field(default=None)

    size: Size = field(default_factory=Size)

    def to_snapshot(self, size_details):
        """
        Capture a snapshot of size details at the time of cart addition.
        """
        self.size_snapshot = {
            "length": size_details.length,
            "width": size_details.width,
            "height": size_details.height,
            "weight": size_details.weight,
        }

    def to_shippo_parcel(self):
        return components.ParcelCreateRequest(
            length = f"{self.length}",  
            width = f"{self.width}",
            height = f"{self.height}",
            weight = f"{self.weight}",
            distance_unit = components.DistanceUnitEnum.IN,
            mass_unit = components.WeightUnitEnum.LB,
        )
    
