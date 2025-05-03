from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.structures import ReviewCollection
from core.review_management.presentation.review_management.models import ProductRating as ProductRatingModel, Review as ReviewModel

from core.review_management.infrastructure.dtos.review_management import PaginatedReviewItemDTO, PaginatedReviewsDTO

from django.core.paginator import Page as DjangoPaginationPage

from typing import Any

class ReviewMapper:
    @staticmethod
    def map_review_into_entity(model: ReviewModel) -> ReviewEntity:
        return ReviewEntity(
                inner_uuid=model.inner_uuid,
                public_uuid=model.public_uuid,
                text=model.text,
                rating=model.rating,
                date_created=model.date_created,
                user=model.user.public_uuid
            )

    @staticmethod
    def map_review_into_dto(model: ReviewModel) -> PaginatedReviewItemDTO:
        return PaginatedReviewItemDTO(
                pub_uuid=model.public_uuid,
                text=model.text,
                rating=model.rating,
                datetime_created=model.date_created,
                username=model.user.username
            )

class ProductRatingMapper:
    @staticmethod
    def map_product_rating_into_entity(model: ProductRatingModel, reviews: ReviewCollection[ReviewEntity] | None = None) -> ProductRatingEntity:
        return ProductRatingEntity(
                inner_uuid=model.inner_uuid,
                public_uuid=model.public_uuid,
                rating=model.rating,
                reviews=reviews if reviews else None,
                product=model.product.public_uuid,
            )

    @staticmethod
    def map_sum_and_count(model: ProductRatingModel, data: dict[str, Any]) -> ProductRatingEntity:
        return ProductRatingEntity(
                inner_uuid=model.inner_uuid,
                public_uuid=model.public_uuid,
                product=model.product.public_uuid,
                total_rating_sum=data["total_rating_sum"],
                total_reviews_count=data["total_reviews_count"]
            )

    @staticmethod
    def map_product_rating_into_dto(page_obj: DjangoPaginationPage, reviews: list[PaginatedReviewItemDTO] | None = None) -> PaginatedReviewsDTO:
        '''
        Django core utils are used for this method!
        '''
        return PaginatedReviewsDTO(
                reviews=reviews if reviews else None,
                current_page=page_obj.number,
                num_pages=page_obj.paginator.num_pages,
                has_previous=page_obj.has_previous(),
                has_next=page_obj.has_next(),
                total_count=page_obj.paginator.count,
            )

