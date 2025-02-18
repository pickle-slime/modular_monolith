from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewRepository, IReviewReadModel
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.value_objects.review_management import ReviewCollection
from core.utils.domain.value_objects.common import ForeignUUID
from core.review_management.presentation.review_management.models import ProductRating as ProductRatingModel, Review as ReviewModel

from django.db.models import Count
from django.core.paginator import Paginator

from typing import Any
import uuid

class DjangoReviewRepository(IReviewRepository):
    @staticmethod
    def map_review_into_entity(model: ReviewModel) -> ReviewEntity:
        return ReviewEntity(
            text=model.text,
            rating=model.rating,
            date_created=model.date_created
        )
    

    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
        try:
            queryset = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid).order_by('-date_created')

            if amount:
                queryset[:amount+1]

            return ReviewCollection([self.map_review_into_entity(model) for model in queryset])
        except ReviewModel.DoesNotExist:
            raise ValueError(f"Review with product rating UUID {product_rating_public_uuid} does not exist.")
        
    # def fetch_rating_product_stars(self, product_rating_inner_uuid) -> tuple[ReviewCollection[ReviewEntity], dict[str, Any]]:
    #     """
    #     Fetch review counts for each rating (1 to 5) and return them as a list of counts.
    #     """
    #     rating_counts = (
    #         ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
    #         .values('rating')
    #         .annotate(count=Count('rating'))
    #     )

    #     return [(self.map_review_into_entity(review), review.count) for review in rating_counts]

    #     return [next((rc['count'] for rc in rating_counts if rc['rating'] == i), 0) for i in range(1, 6)]
    
    def fetch_paginated_reviews(self, product_rating_pub_uuid: uuid.UUID, page_number=1, page_size=5) -> tuple[list[ReviewEntity], dict[str, Any]]:
        """
        Fetches paginated reviews for a given product rating.

        :param product_rating_pub_uuid: UUID of the product rating.
        :param page_number: The current page number (default is 1).
        :param page_size: Number of items per page (default is 5).
        :return: A tuple (reviews, pagination) with paginated reviews and metadata.
        """
        
        reviews_queryset = (
            ReviewModel.objects.filter(product_rating__public_uuid=product_rating_pub_uuid)
            .order_by("-date_created")
        )
        
        paginator = Paginator(reviews_queryset, page_size)
        page_obj = paginator.get_page(page_number)

        reviews = [self.map_review_into_entity(model) for model in page_obj.object_list]
        pagination = {
                'current_page': page_obj.number,
                'num_pages': page_obj.paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'total_count': page_obj.paginator.count
            }
        
        return reviews, pagination

class DjangoProductRatingRepository(IProductRatingRepository):
    @staticmethod
    def map_product_rating_into_entity(model: ProductRatingModel) -> ProductRatingEntity:
        reviews = DjangoReviewRepository()
        product = model.product
        return ProductRatingEntity(
            rating=model.rating,
            reviews=reviews.fetch_reviews_of_product_rating(model.public_uuid),
            product=ForeignUUID(product.inner_uuid, product.public_uuid),
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )
    
    def fetch_rating_by_product_uuid(self, product_inner_uuid: uuid.UUID) -> ProductRatingEntity:
        try:
            model = ProductRatingModel.objects.get(product__inner_uuid=product_inner_uuid)
            return self.map_product_rating_into_entity(model)
        except ProductRatingModel.DoesNotExist:
            return ProductRatingEntity(inner_uuid=None, public_uuid=None)


# CQRS models

class DjangoReviewReadModel(IReviewReadModel):
    """
    A read model (from CQRS context) that handles complex queries within review bounded context
    """
    def fetch_rating_product_stars(self, product_rating_inner_uuid: uuid.UUID) -> tuple[list[Any | int], int]:
        """
        Fetch the count of reviews for each star rating (1 to 5).

        :param product_rating_inner_uuid: UUID of the product rating.
        :return: A list of StarRatingDTO objects, each representing a rating and its count.
        """
        rating_counts = (
            ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
            .values('rating')
            .annotate(count=Count('rating'))
        )

        count = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid).count()
    
        return [next((rc['count'] for rc in rating_counts if rc['rating'] == i), 0) for i in range(5, 0, -1)], count