from core.review_management.domain.aggregates.review_management import ProductRating as ProductRatingEntity
from core.review_management.domain.entities.review_management import Review as ReviewEntity
from core.review_management.domain.structures import ReviewCollection
from core.review_management.presentation.review_management.models import ProductRating as ProductRatingModel, Review as ReviewModel

class ReviewMapper:
    @staticmethod
    def map_review_into_entity(model: ReviewModel) -> ReviewEntity:
        return ReviewEntity(
            text=model.text,
            rating=model.rating,
            date_created=model.date_created
        )
    
class ProductRatingMapper:
    @staticmethod
    def map_product_rating_into_entity(model: ProductRatingModel, reviews: ReviewCollection[ReviewEntity]) -> ProductRatingEntity:
        product = model.product
        return ProductRatingEntity(
            rating=model.rating,
            reviews=reviews,
            product=product.public_uuid,
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
        )
