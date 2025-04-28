from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewReadModel
from core.review_management.application.dtos.review_management import ReviewCollectionDTO

from typing import Any
import uuid

class ProductPageReviewsService:
    def __init__(self, product_rating_repository: IProductRatingRepository, product_rating_read_model: IReviewReadModel):
        self.pr_rep = product_rating_repository
        self.read_model = product_rating_read_model

    def create_review(self, review: dict[str, Any]) -> dict[str, Any]:
        product_rating = self.pr_rep.fetch_rating_by_product_uuid(review.get("product_rating", None))
        product_rating.update_rating()
        rating_list, rating = self.read_model.fetch_rating_product_stars(product_rating_public_uuid=review.get("product_rating", None))
        
        response_data = {
            'rating': rating,
            'rating_list': rating_list,
        }

        return response_data
        
    def load_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number: int) -> dict[str, Any]:
        paginated_reviews = self.pr_rep.fetch_paginated_reviews(product_rating_pub_uuid, page_number)

        return ReviewCollectionDTO.from_paginated_data(paginated_reviews).model_dump(mode="json")
