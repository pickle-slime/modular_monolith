from core.review_management.application.acl.review_management import ProductRatingACL
from core.review_management.infrastructure.repositories.review_management import DjangoProductRatingRepository, DjangoReviewReadModel

class ReivewManagementACLFactory:
    @staticmethod
    def create_product_rating_acl():
        return ProductRatingACL(DjangoProductRatingRepository(), DjangoReviewReadModel())