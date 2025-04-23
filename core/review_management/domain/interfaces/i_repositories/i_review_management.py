from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.structures import ReviewCollection
from core.review_management.infrastructure.dtos.review_management import PaginatedReviewsDTO

from abc import abstractmethod
from typing import Any
import uuid

class IProductRatingRepository(BaseRepository):
    @abstractmethod
    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingEntity:
        pass

    @abstractmethod
    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
        pass

    @abstractmethod
    def fetch_paginated_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number=1, page_size=5) -> PaginatedReviewsDTO:
        pass


class IReviewReadModel(BaseRepository):
    """
    A CQRS read model that handles complex queries within review bounded context
    """
    @abstractmethod
    def fetch_rating_product_stars(
        self, 
        product_rating_inner_uuid: uuid.UUID | None = None, 
        product_rating_public_uuid: uuid.UUID | None = None
    ) -> tuple[list[Any | int], int]:
        pass
