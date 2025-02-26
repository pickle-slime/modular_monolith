from core.review_management.application.dtos.review_management import ProductRatingDTO

from abc import ABC, abstractmethod
from typing import Any
import uuid

class IProductRatingACL(ABC):
    @abstractmethod
    def fetch_rating_by_product_uuid(self, product_public_uuid: uuid.UUID) -> ProductRatingDTO:
        pass

    @abstractmethod
    def fetch_rating_product_stars(self, product_rating_public_uuid) -> tuple[list[Any | int], int]:
        pass

class IReviewACL(ABC):
    pass