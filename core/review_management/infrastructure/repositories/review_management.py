from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewReadModel
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.structures import ReviewCollection
from core.review_management.presentation.review_management.models import ProductRating as ProductRatingModel, Review as ReviewModel
from core.review_management.infrastructure.dtos.review_management import PaginatedReviewsDTO
from ..mappers.review_management import ReviewMapper, ProductRatingMapper

from django.db.models import Count
from django.core.paginator import Paginator

from typing import Any
import uuid


class DjangoProductRatingRepository(IProductRatingRepository):    
    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingEntity:
        try:
            model = ProductRatingModel.objects.get(product__public_uuid=product_public_uuid)
            reviews = self.fetch_reviews_of_product_rating(model.public_uuid)
            return ProductRatingMapper.map_product_rating_into_entity(model, reviews)
        except ProductRatingModel.DoesNotExist:
            return ProductRatingEntity(inner_uuid=None, public_uuid=None)

    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
        try:
            queryset = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid).order_by('-date_created')

            if amount:
                queryset[:amount+1]

            return ReviewCollection([ReviewMapper.map_review_into_entity(model) for model in queryset])
        except ReviewModel.DoesNotExist:
            raise ValueError(f"Review with product rating UUID {product_rating_public_uuid} does not exist.")

    
    def fetch_paginated_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number=1, page_size=5) -> PaginatedReviewsDTO:
        """
        Fetches paginated reviews for a given product rating.

        :product_rating_pub_uuid: UUID of the product rating.
        :page_number: The current page number (default is 1).
        :page_size: Number of items per page (default is 5).
        :return: A tuple (reviews, pagination) with paginated reviews and metadata.
        """
        
        if product_rating_pub_uuid is None:
            return PaginatedReviewsDTO()
        
        reviews_queryset = (
            ReviewModel.objects.filter(product_rating__public_uuid=product_rating_pub_uuid)
            .order_by("-date_created")
        )
        
        paginator = Paginator(reviews_queryset, page_size)
        page_obj = paginator.get_page(page_number)

        reviews = [ReviewMapper.map_review_into_entity(model) for model in page_obj.object_list]
        
        return PaginatedReviewsDTO(
            reviews=reviews,
            current_page=page_obj.number,
            num_pages=page_obj.paginator.num_pages,
            has_previous=page_obj.has_previous(),
            has_next=page_obj.has_next(),
            total_count=page_obj.paginator.count,
        )


# CQRS models

class DjangoReviewReadModel(IReviewReadModel):
    """
    A read CQRS model that handles complex queries within review bounded context
    """
    def fetch_rating_product_stars(
        self, 
        product_rating_inner_uuid: uuid.UUID = None, 
        product_rating_public_uuid: uuid.UUID = None
    ) -> tuple[list[Any | int], int]:
        """
        Fetch the count of reviews for each star rating (1 to 5).

        :param product_rating_inner_uuid: UUID of the product rating.
        :return - a list of StarRatingDTO objects, each representing a rating and its count.
        """
        if product_rating_inner_uuid:
            reviews = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
            count = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid).count()
        elif product_rating_public_uuid:
            reviews = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid)
            count = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid).count()
        else:
            return ([0, 0, 0, 0, 0], 0)
        
        rating_counts = (
            reviews
            .values('rating')
            .annotate(count=Count('rating'))
        )
    
        return [next((rc['count'] for rc in rating_counts if rc['rating'] == i), 0) for i in range(5, 0, -1)], count