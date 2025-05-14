from dataclasses import dataclass, field
from decimal import Decimal
import uuid

#@dataclass(frozen=True)
#class Size:
#    length: Decimal | None = field(default=None)
#    width: Decimal | None = field(default=None)
#    height: Decimal | None = field(default=None)
#    weight: Decimal | None = field(default=None)
#
#    def to_shippo_parcel(self):
#        return components.ParcelCreateRequest(
#            length = f"{self.length}",  
#            width = f"{self.width}",
#            height = f"{self.height}",
#            weight = f"{self.weight}",
#            distance_unit = components.DistanceUnitEnum.IN,
#            mass_unit = components.WeightUnitEnum.LB,
#        )
#
#    @classmethod
#    def map_raw_data(cls, raw_data: dict[str, Any]) -> "Size":
#        return cls(
#                length=raw_data.get("length", None),
#                width=raw_data.get("width", None),
#                height=raw_data.get("height", None),
#                weight=raw_data.get("weight", None)
#            )
 
@dataclass(frozen=True)
class CartItem:
    color: str | None = field(default=None)
    qty: int | None = field(default=None)
    image: str | None = field(default=None)
    price: Decimal | None = field(default=None)

    size: uuid.UUID | None = field(default=None)
   
