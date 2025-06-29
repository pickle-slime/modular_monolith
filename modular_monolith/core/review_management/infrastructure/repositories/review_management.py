from core.review_management.domain.interfaces.i_repositories.i_review_management import IProductRatingRepository, IReviewReadModel
from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.structures import ReviewCollection
from core.review_management.presentation.review_management.models import ProductRating as ProductRatingModel, Review as ReviewModel
from core.review_management.infrastructure.dtos.review_management import PaginatedReviewsDTO
from ..mappers.review_management import ReviewMapper, ProductRatingMapper

from django.db.models import Sum, Count, Avg
from django.core.paginator import Paginator
from django.db import connection, transaction

from dataclasses import asdict
from typing import Any
import uuid


class DjangoProductRatingRepository(IProductRatingRepository):    
    @transaction.atomic()
    def save(self, product_rating_entity: ProductRatingEntity):
        pr_data = asdict(product_rating_entity)
        pr_data.pop("reviews")
        reviews = product_rating_entity.reviews
        self.insert_product_rating(pr_data)

        if reviews:
            review_dicts = []
            for review in reviews:
                review_dict = asdict(review)
                review_dict["product_rating_id"] = product_rating_entity.inner_uuid
                review_dict["user_id"] = review_dict.pop("user", None)
                review_dicts.append(review_dict)
            self.bulk_insert_reviews(review_dicts)

    def bulk_insert_reviews(self, review_dicts: list[dict]):
        insert_sql = '''
            INSERT INTO review_management_review (
                inner_uuid, public_uuid, text, rating, date_created, product_rating_id, user_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (inner_uuid) DO NOTHING
        '''

        values = [
            (
                review["inner_uuid"],
                review["public_uuid"],
                review["text"],
                review["rating"],
                review["date_created"],
                review["product_rating_id"],
                review["user_id"],
            )
            for review in review_dicts
        ]

        with connection.cursor() as cursor:
            for value in values:
                cursor.execute(insert_sql, value)

    def insert_product_rating(self, pr_data: dict):
        sql = '''
            INSERT INTO review_management_productrating (
                inner_uuid, public_uuid, rating, product_id
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (inner_uuid) DO UPDATE SET
                rating = EXCLUDED.rating
        '''
        values = (
            pr_data["inner_uuid"],
            pr_data["public_uuid"],
            pr_data["rating"],
            pr_data["product"],
        )

        with connection.cursor() as cursor:
            cursor.execute(sql, values)

    def fetch_via_public_uuid(self, pub_uuid: uuid.UUID, include_reviews: bool = False) -> ProductRatingEntity:
        try:
            model = ProductRatingModel.objects.get(public_uuid=pub_uuid)
            reviews = self.fetch_reviews_of_product_rating(model.public_uuid)
            if include_reviews:
                return ProductRatingMapper.map_product_rating_into_entity(model, reviews)
            else:
                return ProductRatingMapper.map_product_rating_into_entity(model)
        except ProductRatingModel.DoesNotExist:
            return ProductRatingEntity()

    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingEntity:
        try:
            model = ProductRatingModel.objects.get(product__public_uuid=product_public_uuid)
            reviews = self.fetch_reviews_of_product_rating(model.public_uuid)
            return ProductRatingMapper.map_product_rating_into_entity(model, reviews)
        except ProductRatingModel.DoesNotExist:
            return ProductRatingEntity()

    def fetch_reviews_of_product_rating(self, product_rating_public_uuid: uuid.UUID, amount: int | None = None) -> ReviewCollection[ReviewEntity]:
        try:
            queryset = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid).order_by('-date_created')

            if amount:
                queryset[:amount+1]

            return ReviewCollection([ReviewMapper.map_review_into_entity(model) for model in queryset])
        except ReviewModel.DoesNotExist:
            raise ValueError(f"Review with product rating UUID {product_rating_public_uuid} does not exist.")


# CQRS models

class DjangoReviewReadModel(IReviewReadModel):
    """
    A read CQRS model that handles complex queries within review bounded context
    """
    def fetch_rating_product_stars(
                self, 
                product_rating_inner_uuid: uuid.UUID | None = None, 
                product_rating_public_uuid: uuid.UUID | None = None
            ) -> tuple[list[Any | int], float]:
        """
        Fetchs a tuple of amounts of stars for all reviews (1 to 5).

        :param - product_rating_inner_uuid: inner UUID of the product rating.
        :param - product_rating_public_uuid: public UUID of the product rating.

        :return - a tuple of list with amount of reviews per each star and average rating.

        :raises ValueError - If neither inner nor public UUID is provided.
        """

        if product_rating_inner_uuid:
            reviews = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
        elif product_rating_public_uuid:
            reviews = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid)
        else:
            raise ValueError("At least one of product_rating_inner_uuid or product_rating_public_uuid must be provided.")
        
        avg = reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0
        rating_counts = (
            reviews
            .values('rating')
            .annotate(count=Count("inner_uuid"))
        )
    
        return [next((rc['count'] for rc in rating_counts if rc['rating'] == i), 0) for i in range(5, 0, -1)], avg

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

        if product_rating_inner_uuid:
            reviews = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
        elif product_rating_public_uuid:
            reviews = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid)
        else:
            raise ValueError("At least one of product_rating_inner_uuid or product_rating_public_uuid must be provided.")

        return reviews.count()

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

        if product_rating_inner_uuid:
            product_rating = ProductRatingModel.objects.get(inner_uuid=product_rating_inner_uuid)
            reviews = ReviewModel.objects.filter(product_rating__inner_uuid=product_rating_inner_uuid)
        elif product_rating_public_uuid:
            product_rating = ProductRatingModel.objects.get(public_uuid=product_rating_public_uuid)
            reviews = ReviewModel.objects.filter(product_rating__public_uuid=product_rating_public_uuid)
        else:
            raise ValueError("At least one of product_rating_inner_uuid or product_rating_public_uuid must be provided.")
        
        data = reviews.aggregate(total_rating_sum=Sum("rating"), total_reviews_count=Count("inner_uuid"))

        return ProductRatingMapper.map_sum_and_count(product_rating, data)


    def fetch_paginated_reviews(self, product_rating_pub_uuid: uuid.UUID | None, page_number=1, page_size=5) -> PaginatedReviewsDTO:
        """
        Fetches paginated reviews for a given product rating.

        :product_rating_pub_uuid - UUID of the product rating.
        :page_number - The current page number (default is 1).
        :page_size - Number of items per page (default is 5).
        :return - A tuple (reviews, pagination) with paginated reviews and metadata.
        """
        
        if product_rating_pub_uuid is None:
            return PaginatedReviewsDTO()
        
        reviews_queryset = (
            ReviewModel.objects.filter(product_rating__public_uuid=product_rating_pub_uuid)
            .order_by("-date_created")
        )
        
        paginator = Paginator(reviews_queryset, page_size)
        page_obj = paginator.get_page(page_number)

        reviews = [ReviewMapper.map_review_into_dto(model) for model in page_obj.object_list]
        
        return ProductRatingMapper.map_product_rating_into_dto(page_obj, reviews)
