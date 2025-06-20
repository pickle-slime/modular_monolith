from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewReadModel
from core.review_management.application.dtos.review_management import ReviewCollectionDTO

from core.review_management.application.exceptions import MissingProductRatingError

from typing import Any
import uuid

class ProductPageReviewsService:
    def __init__(self, product_rating_repository: IProductRatingRepository, product_rating_read_model: IReviewReadModel):
        self.pr_rep = product_rating_repository
        self.read_model = product_rating_read_model

    def create_review(self, review: dict[str, Any]) -> dict[str, Any]:
        product_rating_pub_uuid = review.get("product_rating", None)
        if product_rating_pub_uuid is None:
            raise MissingProductRatingError(f"{self.__class__.__name__}.{self.create_review.__name__} didn't get review/'s proudct rating")

        product_rating = self.read_model.fetch_sum_and_count(product_rating_public_uuid=product_rating_pub_uuid)
        product_rating.add_review(review)
        self.pr_rep.save(product_rating)
        rating_list, rating = self.read_model.fetch_rating_product_stars(product_rating_public_uuid=product_rating_pub_uuid)

        response_data = {
            'rating': rating,
            'rating_list': rating_list,
        }

        return response_data
        
    def load_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number: int) -> dict[str, Any]:
        paginated_reviews = self.read_model.fetch_paginated_reviews(product_rating_pub_uuid, page_number)

        return ReviewCollectionDTO.from_paginated_data(paginated_reviews).model_dump(mode="json", by_alias=True)
