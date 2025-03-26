from shippo import components

from dataclasses import dataclass, field
from decimal import Decimal

@dataclass(frozen=True)
class Size:
    length: Decimal | None = field(default=None)
    width: Decimal | None = field(default=None)
    height: Decimal | None = field(default=None)
    weight: Decimal | None = field(default=None)

    def to_shippo_parcel(self):
        return components.ParcelCreateRequest(
            length = f"{self.length}",  
            width = f"{self.width}",
            height = f"{self.height}",
            weight = f"{self.weight}",
            distance_unit = components.DistanceUnitEnum.IN,
            mass_unit = components.WeightUnitEnum.LB,
        )
 
@dataclass(frozen=True)
class CartItem:
    color: str | None = field(default=None)
    qty: int | None = field(default=None)
    image: str | None = field(default=None)
    price: Decimal | None = field(default=None)

    size: Size = field(default_factory=Size)
   
