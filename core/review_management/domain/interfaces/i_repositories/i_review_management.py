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
    def save(self, product_rating_entity: ProductRatingEntity):
        pass

    @abstractmethod
    def fetch_via_public_uuid(self, pub_uuid: uuid.UUID, include_reviews: bool) -> ProductRatingEntity:
        pass

    @abstractmethod
    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingEntity:
        pass

    @abstractmethod
    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
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
        """
        Fetchs a tuple of amounts of stars for all reviews (1 to 5).

        :param - product_rating_inner_uuid: inner UUID of the product rating.
        :param - product_rating_public_uuid: public UUID of the product rating.

        :return - a tuple of list with amount of reviews per each star and average rating.

        :raises ValueError - If neither inner nor public UUID is provided.
        """

        pass

    @abstractmethod
    def fetch_reviews_count(
                self, 
                product_rating_inner_uuid: uuid.UUID | None = None, 
                product_rating_public_uuid: uuid.UUID | None = None
            ) -> int:
        '''
        Fetches count of all reviews for provided product rating
        
        :param - product_rating_inner_uuid: inner UUID of the product rating.
        :param - product_rating_public_uuid: public UUID of the product rating.

        :return - count of all reviews

        :raises ValueError - If neither inner nor public UUID is provided.
        '''

        pass

    @abstractmethod
    def fetch_sum_and_count(
                self, 
                product_rating_inner_uuid: uuid.UUID | None = None, 
                product_rating_public_uuid: uuid.UUID | None = None
            ) -> ProductRatingEntity:
        '''
        Fetches count and rating sum for all reviews with the provided product rating
        
        :param - product_rating_inner_uuid: inner UUID of the product rating.
        :param - product_rating_public_uuid: public UUID of the product rating.

        :return - count of all reviews and rating sum

        :raises ValueError - If neither inner nor public UUID is provided.
        '''
        pass

    @abstractmethod
    def fetch_paginated_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number=1, page_size=5) -> PaginatedReviewsDTO:
        pass


