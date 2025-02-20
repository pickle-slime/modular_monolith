from .....utils.domain.interfaces.i_repositories.base_repository import BaseRepository
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.value_objects.review_management import ReviewCollection

from abc import abstractmethod
from typing import Any
import uuid

class IProductRatingRepository(BaseRepository):
    @abstractmethod
    def fetch_rating_by_product_uuid(self, product_inner_uuid: uuid.UUID) -> ProductRatingEntity:
        pass

class IReviewRepository(BaseRepository):
    @abstractmethod
    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
        pass

    @abstractmethod
    def fetch_paginated_reviews(self, product_rating_pub_uuid, page_number=1, page_size=5) -> tuple[list[ReviewEntity], dict[str, Any]]:
        pass


class IReviewReadModel(BaseRepository):
    """
    A read model (from CQRS context) that handles complex queries within review bounded context
    """
    @abstractmethod
    def fetch_rating_product_stars(self, product_rating_inner_uuid: uuid.UUID) -> tuple[list[Any | int], int]:
        pass