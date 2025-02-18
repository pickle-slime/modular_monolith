from ....utils.domain.entity import Entity
from ..entities.review_management import Review
from ..value_objects.review_management import ReviewCollection
from ....utils.domain.value_objects.common import ForeignUUID

from dataclasses import dataclass, field
from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class ProductRating(Entity):
    rating: Decimal = field(default=Decimal("0.0"))
    reviews: ReviewCollection[Review] = field(default_factory=ReviewCollection)
    product: ForeignUUID | uuid.UUID = field(default=None)

    def update_rating(self):
        if not self.reviews:
            self.rating = Decimal("0.0")
        else:
            total = sum(review.rating for review in self.reviews)
            self.rating = total / len(self.reviews)
