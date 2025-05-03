from pydantic import Field
from datetime import datetime
from decimal import Decimal
import uuid

from stripe import Review

from core.utils.application.base_dto import BaseEntityDTO, BaseDTO
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from ...infrastructure.dtos.review_management import PaginatedReviewsDTO, PaginatedReviewItemDTO
from core.review_management.domain.structures import ReviewCollection

class ReviewDTO(BaseEntityDTO["ReviewDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)

    text: str | None = Field(default=None, min_length=1, max_length=10000, title="Text")
    rating: int | None = Field(default=None, ge=0, le=5, title="Rating")
    datetime_created: datetime | None = Field(default=None, title="DateTime Created")

    user: uuid.UUID | None = Field(default=None, title="User", description="Contains a public uuid of external module")

    @staticmethod
    def from_entity(review: ReviewEntity) -> 'ReviewDTO':
        return ReviewDTO(
            pub_uuid=review.public_uuid,
            text=review.text,
            rating=review.rating,
            datetime_created=review.date_created,
            user=review.user,
        )

    @staticmethod
    def from_entities(reviews: list[ReviewEntity]| ReviewCollection[ReviewEntity] | None) -> list['ReviewDTO'] | None:
        if reviews :
            return [ReviewDTO.from_entity(review) for review in reviews]
        return None

class ProductRatingDTO(BaseEntityDTO["ProductRatingDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)

    rating: Decimal | None = Field(default=None, ge=0, le=5, title="Rating")
    reviews: list[ReviewDTO] | None = Field(default=None, title="Reviews")
    
    product: uuid.UUID | None = Field(default=None, title="Product", description="Contains a public uuid of external module")

    @staticmethod
    def from_entity(product_rating: ProductRatingEntity | None, pagination: dict | None = None) -> 'ProductRatingDTO':
        return ProductRatingDTO(
            pub_uuid=product_rating.public_uuid,
            rating=product_rating.rating,
            reviews=ReviewCollectionDTO.from_paginated_data(product_rating.reviews, pagination) if pagination else ReviewDTO.from_entities(product_rating.reviews),
            product=product_rating.product,
        )

class ReviewItemDTO(BaseEntityDTO["ReviewItemDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)

    text: str | None = Field(default=None, min_length=1, max_length=10000, title="Text", alias="text")
    rating: int | None = Field(default=None, ge=0, le=5, title="Rating", alias="rating")
    datetime_created: str | None = Field(default=None, title="DateTime Created", alias="datetimeCreated")

    username: str | None = Field(default=None, title="User", description="Contains owner's name", alias="username")

    @classmethod
    def from_entity(cls, review: PaginatedReviewItemDTO) -> 'ReviewItemDTO':
        return cls(
            pub_uuid=review.pub_uuid,
            text=review.text,
            rating=review.rating,
            datetime_created=cls.format_datetime(datetime=review.datetime_created),
            username=review.username,
        )
    
    @staticmethod
    def from_entities(reviews: list[PaginatedReviewItemDTO] | None) -> list['ReviewItemDTO'] | None:
        if reviews :
            return [ReviewItemDTO.from_entity(review) for review in reviews]
        return None

    @classmethod
    def format_datetime(cls, datetime: datetime | None, format_str: str = "%d %B %Y, %-I:%M %p") -> str | None:
        if datetime:
            return datetime.strftime(format_str)
        else:
            return None
 
class ReviewCollectionDTO(BaseDTO[ReviewItemDTO]):
    reviews: list[ReviewItemDTO] | None = Field(default=None, title="Reviews", alias="reviews")
    current_page: int | None = Field(default=None, ge=0, title="Current Page", alias="currentPage")
    num_pages: int | None = Field(default=None, ge=0, title="Number of Pages", alias="numPages")
    has_previous: bool | None = Field(default=None, title="Has Previous", alias="hasPrevious")
    has_next: bool | None = Field(default=None, title="Has Next", alias="hasNext")
    total_count: int | None = Field(default=None, ge=0, title="Total Count", alias="totalCount")

    @classmethod
    def from_paginated_data(cls, paginated_reviews: PaginatedReviewsDTO) -> 'ReviewCollectionDTO':
        return cls(
            reviews=ReviewItemDTO.from_entities(paginated_reviews.reviews),
            current_page=paginated_reviews.current_page,
            num_pages=paginated_reviews.num_pages,
            has_previous=paginated_reviews.has_previous,
            has_next=paginated_reviews.has_next,
            total_count=paginated_reviews.total_count,
        )


