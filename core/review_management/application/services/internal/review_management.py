from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator

from core.review_management.presentation.review_management.forms import ReviewForm
from core.review_management.domain.interfaces.i_repositories.i_review_management import IReviewRepository
from core.review_management.application.dtos.review_management import ReviewCollectionDTO

from typing import Any
import json
import uuid

class ProductPageReviewsService:
    def __init__(self, review_repository: IReviewRepository):
        self.review_rep = review_repository

    def create_review(self, review: dict[str, Any]) -> dict[str, Any]:
        rating_list = self.review_rep.fetch_rating_counts_as_list(review.product_rating)
        
        response_data = {
            'rating': review.product_rating.rating,
            'rating_list': rating_list,
        }
        return response_data
        
    def load_reviews(self, product_rating_pub_uuid: uuid.UUID | str, page_number: int) -> dict[str, Any]:
        if product_rating_pub_uuid:
            review_entities, pagination = self.review_rep.fetch_paginated_reviews(product_rating_pub_uuid, page_number)
        else:
            review_entities, pagination = list(), 0

        return ReviewCollectionDTO.from_paginated_data(review_entities, pagination).model_dump(mode="json")