from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewReadModel
from core.review_management.domain.interfaces.i_acl import IProductRatingACL
from core.review_management.application.dtos.review_management import ProductRatingDTO

from typing import Any
import uuid

class ProductRatingACL(IProductRatingACL):
    def __init__(self, product_rating_repository: IProductRatingRepository, review_read_model: IReviewReadModel):
        self.pr_rep = product_rating_repository
        self.review_read_model = review_read_model

    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingDTO:
        return ProductRatingDTO.from_entity(self.pr_rep.fetch_rating_by_product_uuid(product_public_uuid))
    
    def fetch_rating_product_stars(self, product_rating_public_uuid: uuid.UUID) -> tuple[list[Any | int], int]:
        return self.review_read_model.fetch_rating_product_stars(product_rating_public_uuid=product_rating_public_uuid)

    def fetch_reviews_count(self, product_rating_public_uuid: uuid.UUID) -> int:
        return self.review_read_model.fetch_reviews_count(product_rating_public_uuid=product_rating_public_uuid)
