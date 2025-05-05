from core.utils.domain.entity import Entity
from ..entities.review_management import Review
from ..structures import ReviewCollection
from ..exceptions import MissingFieldDataError

from dataclasses import dataclass, field
from typing import Any
from decimal import Decimal
import uuid

@dataclass(kw_only=True)
class ProductRating(Entity):
    rating: Decimal | None = field(default=None)
    reviews: ReviewCollection[Review] | None = field(default=None)

    product: uuid.UUID | None = field(default=None)

    #fields below are used for more efficient calculation and aren't a part of the aggregate
    total_rating_sum: Decimal | None = field(default=Decimal("0.0"))
    total_reviews_count: int | None = field(default=0)

    review: type[Review] = Review

    def add_review(self, raw_review: dict[str, Any]):
        if self.reviews is None:
            self.reviews = ReviewCollection([])

        review = self.review.map(raw_review)
        self.reviews.append(review)

        if review.rating is not None:
            self.total_rating_sum = (self.total_rating_sum or Decimal("0.0")) + Decimal(review.rating)
            self.total_reviews_count = (self.total_reviews_count or 0) + 1

        self.update_rating()

    def update_rating(self):
        if self.total_rating_sum is None :
            raise MissingFieldDataError(f"{self.__class__.__name__}.{self.update_rating.__name__}: There is no self.total_rating_sum data present")
        elif self.total_reviews_count is None:
            raise MissingFieldDataError(f"{self.__class__.__name__}.{self.update_rating.__name__}: There is no self.total_reviews_count data present")
        
        if self.total_reviews_count == 0:
            self.rating = Decimal("0.0")
        else:
            self.rating = self.total_rating_sum / Decimal(self.total_reviews_count)

