from pydantic import BaseModel, Field
from typing import Generic
from datetime import datetime
from decimal import Decimal
import uuid

from core.utils.application.base_dto import BaseEntityDTO, DTO
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from ...infrastructure.dtos.review_management import PaginatedReviewsDTO
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
            user=None,
        )
    
    @staticmethod
    def from_entities(reviews: list[ReviewEntity]| ReviewCollection[ReviewEntity] | None) -> list['ReviewDTO'] | None:
        if reviews :
            return [ReviewDTO.from_entity(review) for review in reviews]
        return None

class ReviewCollectionDTO(BaseModel, Generic[DTO]):
    reviews: list[ReviewDTO] | None = Field(default=None, title="Reviews")
    current_page: int | None = Field(default=None, ge=0, title="Current Page", alias="currentPage")
    num_pages: int | None = Field(default=None, ge=0, title="Number of Pages", alias="numPages")
    has_previous: bool | None = Field(default=None, title="Has Previous", alias="hasPrevious")
    has_next: bool | None = Field(default=None, title="Has Next", alias="hasNext")
    total_count: int | None = Field(default=None, ge=0, title="Total Count", alias="totalCount")

    @staticmethod
    def from_paginated_data(paginated_reviews: PaginatedReviewsDTO) -> 'ReviewCollectionDTO':
        return ReviewCollectionDTO(
            reviews=ReviewDTO.from_entities(paginated_reviews.reviews),
            current_page=paginated_reviews.current_page,
            num_pages=paginated_reviews.num_pages,
            has_previous=paginated_reviews.has_previous,
            has_next=paginated_reviews.has_next,
            total_count=paginated_reviews.total_count,
        )

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