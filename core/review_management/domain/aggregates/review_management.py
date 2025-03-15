from core.utils.domain.entity import Entity
from ..entities.review_management import Review
from ..structures import ReviewCollection

from dataclasses import dataclass, field
from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class ProductRating(Entity):
    rating: Decimal = field(default=None)
    reviews: ReviewCollection[Review] = field(default=None)
    product: uuid.UUID = field(default=None)

    def add_review(self, review: Review):
        self.reviews.append(review)
        self.update_rating()

    def update_rating(self):
        if not self.reviews:
            self.rating = Decimal("0.0")
        else:
            total = sum(review.rating for review in self.reviews)
            self.rating = total / len(self.reviews)
